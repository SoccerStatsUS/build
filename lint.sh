#!/bin/sh
# Run the static check across every sibling repo that configures one.
#
# Counts are expected to be non-zero: the findings are a standing backlog, not a
# regression, and each repo works its own down. See the repo ROADMAPs.
#
# The ruff version is pinned because different versions find different things,
# which would make the counts drift on their own.

cd "$(dirname "$0")/.." || exit 1

for cfg in */ruff.toml; do
    repo=${cfg%/ruff.toml}
    n=$(uvx ruff@0.16.1 check --output-format concise "$repo" 2>/dev/null \
        | grep -cE ':[0-9]+:[0-9]+:')
    printf '%-12s %4s\n' "$repo" "$n"
done
