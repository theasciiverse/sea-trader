#!/bin/sh
# Builds Sea Trader for the Asciiverse catalog into stage/: one executable
# made with `bun build --compile`, which carries the Bun runtime, the game
# and every library it uses, so players install nothing (no Node, no npm).
#
#   npm ci --ignore-scripts
#   sh asciiverse/build.sh [BUN_TARGET] [OUTPUT_NAME]
#
# BUN_TARGET is a `bun build --target`, such as bun-linux-x64-baseline,
# bun-darwin-arm64 or bun-windows-x64-baseline (default: this machine);
# OUTPUT_NAME defaults to sea-trader (sea-trader.exe for Windows).
#
# Needs Bun 1.2 and the packages from `npm ci`. Ink lays out the screen with
# yoga-wasm-web, whose Node entry reads yoga.wasm from beside itself at run
# time; that file is not inside a compiled executable, so the entry is
# changed in node_modules to import the WebAssembly file instead, which Bun
# then embeds. React is built for production. Ink connects to React's
# developer tools when DEV=true; its devtools.js is emptied so they are
# not built in (left as an external import, Bun loads it at start).
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"
target=${1:-}
out=${2:-sea-trader}

yoga=node_modules/yoga-wasm-web/dist/node.js
if ! grep -q 'yoga.wasm" with' "$yoga"; then
  sed -i.orig 's|let Yoga=await a(await E(_(import.meta.url).resolve("./yoga.wasm")));|import yogaWasm from "./yoga.wasm" with { type: "file" };let Yoga=await a(await E(yogaWasm));|' "$yoga"
  grep -q 'yoga.wasm" with' "$yoga" || { echo "build.sh: $yoga has changed, the yoga.wasm patch did not apply" >&2; exit 1; }
fi

printf 'export {};\n' > node_modules/ink/build/devtools.js

rm -rf stage
mkdir -p stage
bun build src/cli.tsx --compile --minify \
  --define 'process.env.NODE_ENV="production"' \
  ${target:+--target="$target"} \
  --outfile "stage/$out"
cp LICENSE CHANGELOG.md PATCHES.md stage/
cp asciiverse/README.md stage/README.md
ls -l stage
