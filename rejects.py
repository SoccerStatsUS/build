"""
Structured record of every point where the build gives up on a row.

The loaders and parsers signal bad data by calling pdb.set_trace(). That is
useful at a terminal and useless in a batch run, where the only thing it can
report is a filename and a line number. install() replaces set_trace with a
recorder that also captures the caller's local variables, so the build says
which row was bad instead of only where the code was standing.

Records are written as JSON lines to logs/rejects.jsonl. Nothing is raised;
the build continues exactly as it did before.
"""

import datetime
import json
import os
import sys
import traceback


LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'rejects.jsonl')

# A single bad file can hit the same site thousands of times. Keep counting
# past the cap, but stop writing payloads; the first few are representative.
PAYLOADS_PER_SITE = 50

MAX_STRING = 200
MAX_ITEMS = 8

_stage = None
_handle = None
_path = None
_counts = {}


def set_stage(name):
    """Name the pipeline step now running (load, normalize, merge, ...)."""
    global _stage
    _stage = name


def install(path=LOG_PATH):
    """Point pdb.set_trace at the recorder and start a fresh log."""
    global _handle, _path

    import pdb

    os.makedirs(os.path.dirname(path), exist_ok=True)
    _handle = open(path, 'w', buffering=1)
    _path = path
    _counts.clear()

    pdb.set_trace = _record_set_trace


def _record_set_trace(*args, **kwargs):
    caller = traceback.extract_stack()[-2]
    site = '%s:%s' % (caller.filename, caller.lineno)

    seen = _counts.get(site, 0)
    _counts[site] = seen + 1

    # Keep the old line so build.sh's grep still finds it.
    print('DATA WARNING (skipped pdb): %s in %s' % (site, caller.name))

    if _handle is None or seen >= PAYLOADS_PER_SITE:
        return

    try:
        f_locals = sys._getframe(1).f_locals
    except ValueError:
        f_locals = {}

    row = {
        'stage': _stage,
        'file': caller.filename,
        'line': caller.lineno,
        'func': caller.name,
        'source': caller.line,
        'locals': _safe_dict(f_locals),
    }

    _handle.write(json.dumps(row) + '\n')


def _safe_dict(d):
    out = {}
    for k, v in list(d.items())[:30]:
        if k.startswith('__'):
            continue
        v = _safe(v)
        if v is not _SKIP:
            out[k] = v
    return out


class _Skip(object):
    pass


_SKIP = _Skip()


def _safe(v, depth=0):
    """Reduce a local variable to something small and JSON-serializable."""

    if v is None or isinstance(v, (bool, int, float)):
        return v

    if isinstance(v, str):
        return v[:MAX_STRING]

    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()

    if callable(v) or isinstance(v, type(sys)):
        return _SKIP

    if depth >= 2:
        return _repr(v)

    if isinstance(v, dict):
        return {str(k)[:MAX_STRING]: _safe(x, depth + 1) for k, x in list(v.items())[:MAX_ITEMS]}

    if isinstance(v, (list, tuple, set)):
        return [_safe(x, depth + 1) for x in list(v)[:MAX_ITEMS]]

    return _repr(v)


def _repr(v):
    try:
        return repr(v)[:MAX_STRING]
    except Exception:
        return '<unreprable %s>' % type(v).__name__


def summary():
    """Sites that fired, most frequent first."""
    return sorted(_counts.items(), key=lambda kv: -kv[1])


def print_summary():
    if _handle is not None:
        _handle.flush()

    total = sum(_counts.values())
    print()
    print('--- rejects: %d from %d sites (%s) ---' % (total, len(_counts), _path))
    for site, count in summary():
        print('%7d  %s' % (count, site))
    if not _counts:
        print('none')
