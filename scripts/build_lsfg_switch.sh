#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$root/github_repos/drastic-lsfg"
revision=ebee4ceefe0bdadb0c564986098f29a58dc4baf6
build_dir="$root/build/lsfg-switch"
if [[ ! -d "$source_dir/.git" ]]; then
    git init -q "$source_dir"
fi
if [[ "$(git -C "$source_dir" rev-parse --verify HEAD 2>/dev/null)" != "$revision" ]]; then
    git -C "$source_dir" fetch -q --depth 1 https://github.com/NaGaa95/DrasticDS_nx.git "$revision"
    git -C "$source_dir" checkout -q --detach FETCH_HEAD
fi
cmake -S "$source_dir/source/deko_compiler" -B "$build_dir" \
    -DCMAKE_TOOLCHAIN_FILE="$DEVKITPRO/cmake/Switch.cmake" -DCMAKE_BUILD_TYPE=Release
cmake --build "$build_dir" --parallel "${BUILD_JOBS:-$(nproc)}" --target lsfg uam_isolate
