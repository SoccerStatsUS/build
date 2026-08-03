#!/bin/bash
# Build the mongo database from the data repos.
# Writes everything to logs/build.log as well as the terminal.
set -e
cd "$(dirname "$0")"

mkdir -p logs
LOG=logs/build.log
exec > >(tee "$LOG") 2>&1

echo "build started $(date)"

# Tests first: they take a tenth of a second and need no mongo, so there is no
# reason to spend 75 seconds building on code that is already known broken.
# SKIP_TESTS=1 ./build.sh to build anyway, mid-refactor.
if [ -z "$SKIP_TESTS" ]; then
    .venv/bin/python -m pytest -q
fi

# stdin is /dev/null so make/__main__.py stubs pdb instead of blocking on it.
# `|| status=$?` keeps set -e from skipping the summary when the build fails.
status=0
PYTHONPATH=~/soccer:~/soccer/build .venv/bin/python -u make/ < /dev/null || status=$?

echo "build finished $(date)"

echo
echo "--- data warnings, deduped ---"
grep 'DATA WARNING' "$LOG" | sort | uniq -c | sort -rn || echo "none"

exit $status
