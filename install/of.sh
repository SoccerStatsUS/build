#!/bin/sh
set -eu

soccer_dir=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
data_dir="$soccer_dir/openfootball"

mkdir -p "$data_dir"

for repo in world champions-league england espana deutschland italy europe; do
    target="$data_dir/$repo"
    if [ -d "$target/.git" ]; then
        git -C "$target" pull --ff-only
    else
        git clone "https://github.com/openfootball/$repo.git" "$target"
    fi
done
