import atexit
import os
import pdb
import sys
import traceback

# Locals the parsers keep the current data line in, best first.
LINE_LOCALS = ('line', 's', 'remainder', 'text')
PATH_LOCALS = ('p', 'path', 'filename')

WARNING_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'logs', 'data_warnings.txt')

warnings = []


def find_data_context(frame):
    """
    Walk out from the parser frame collecting the data that failed:
    the fragment at hand, the whole line it came from, and the file.

    The parsers pass a line down through several methods, narrowing it as
    they go, so the innermost string is the fragment and the outermost is
    the line as the file has it.
    """
    fragment = line = path = None

    while frame:
        local = frame.f_locals

        for name in LINE_LOCALS:
            value = local.get(name)
            if isinstance(value, str) and value.strip():
                if fragment is None:
                    fragment = value.strip()
                line = value.strip()
                break

        if path is None:
            for name in PATH_LOCALS:
                value = local.get(name)
                if isinstance(value, str) and os.path.isfile(value):
                    path = value
                    break

        frame = frame.f_back

    return fragment, line, path


def loose(s):
    """A data line as the parsers see it, after their cleanups."""
    return s.replace('*', '').replace('\xa0', '').replace('\xc2', '').replace(' ', '').strip()


def find_line_number(path, line):
    """Line number of a data line, or None if it can't be pinned down."""

    if not (path and line):
        return None

    try:
        lines = open(path).read().split('\n')
    except OSError:
        return None

    # The parsers strip and clean lines as they go, so fall back to a
    # comparison that does the same to both sides.
    for match in (lambda l: l.strip() == line, lambda l: loose(l) == loose(line)):
        for number, l in enumerate(lines, 1):
            if match(l):
                return number

    return None


def warn(*args, **kwargs):
    """
    Stand in for pdb.set_trace().

    The parsers drop into pdb when data looks wrong. In a non-interactive
    run there is no terminal to debug in, so record what failed and carry on.
    """
    caller = traceback.extract_stack()[-2]
    fragment, line, path = find_data_context(sys._getframe(1))
    number = find_line_number(path, line)

    if fragment and line and loose(fragment) == loose(line):
        fragment = None

    warnings.append({
        'parser': '%s:%s in %s' % (caller.filename, caller.lineno, caller.name),
        'path': path,
        'number': number,
        'line': line,
        'fragment': fragment,
        })

    where = path or 'unknown file'
    if number:
        where = '%s:%s' % (where, number)
    print('DATA WARNING (skipped pdb): %s' % where)
    print('  parser: %s:%s in %s' % (caller.filename, caller.lineno, caller.name))
    if line:
        print('  line: %s' % line)
    if fragment:
        print('  at: %s' % fragment)


def report():
    """Print every skipped line again at the end, and leave a copy behind."""

    if not warnings:
        return

    out = ['%s data lines skipped' % len(warnings), '']
    for w in warnings:
        where = w['path'] or 'unknown file'
        if w['number']:
            where = '%s:%s' % (where, w['number'])
        out.append(where)
        out.append('  parser: %s' % w['parser'])
        if w['line']:
            out.append('  line: %s' % w['line'])
        if w['fragment']:
            out.append('  at: %s' % w['fragment'])
        out.append('')

    text = '\n'.join(out)
    print()
    print(text)

    try:
        open(WARNING_LOG, 'w').write(text)
        print('written to %s' % WARNING_LOG)
    except OSError as e:
        print('could not write %s: %s' % (WARNING_LOG, e))


if not sys.stdin.isatty():
    pdb.set_trace = warn
    atexit.register(report)

from main import build

build()
