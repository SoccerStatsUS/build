import sys

from build import rejects

# The parsers drop into pdb when data looks wrong. In a non-interactive run
# there is no terminal to debug in, so record the row and continue.
if not sys.stdin.isatty():
    rejects.install()

from main import build

build()

rejects.print_summary()
