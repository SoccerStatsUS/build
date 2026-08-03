import pdb
import sys
import traceback

# The parsers drop into pdb when data looks wrong. In a non-interactive
# run there is no terminal to debug in, so log the location and continue.
if not sys.stdin.isatty():
    def _warn_set_trace(*args, **kwargs):
        caller = traceback.extract_stack()[-2]
        print('DATA WARNING (skipped pdb): %s:%s in %s' % (caller.filename, caller.lineno, caller.name))
    pdb.set_trace = _warn_set_trace

from main import build

build()
