# Changes from upstream

This is the Asciiverse packaging of
[Sea Trader](https://github.com/zyishai/sea-trader) by Yishai Zehavi
(zyishai), a trading voyage through the 19th-century South China Sea in
TypeScript on Ink and XState, published on npm as `ctrader`. Upstream is
the `upstream` remote; the `asciiverse` branch starts at upstream's tag
`v3.2.0` (2026-10-12), so our tags are `v3.2.0-av.N`. Upstream's LICENSE
(MIT) keeps the template's "[year] [fullname]" copyright line; the author
is Yishai Zehavi, as `package.json` says.

## The game

Unchanged: rules, numbers, texts and screens are upstream's. Only the
lettering of three titles is drawn by a different library (below), in the
same style.

## Saves, settings and logs

None to move. Sea Trader writes no files (a voyage lasts one sitting, and
the start screen's options live in memory) and makes no network
connections.

## Ours

- **Title lettering through figlet.js, its fonts built in**
  (`src/terminal/figlet-fonts.ts`, `src/figlet-fonts.d.ts`, `StartScreen`,
  `HelpScreen`, `ViewTitle`). The start and help screens drew "Sea Trader"
  and "How to play" with ink-big-text, which uses cfonts (GPL-3.0-or-later)
  and reads its font files from disk; the screen titles used figlet.js,
  which also read its "Standard" font from disk. Both now come from
  figlet.js with the "Small" (in capitals, as cfonts drew it) and
  "Standard" fonts imported as modules, so
  the single executable finds them and everything in it is under MIT or
  similar terms. "Small" is the figlet font cfonts' "simple" follows, so
  the lettering looks the same. ink-big-text stays in `package.json` and
  the lockfile for now, unused, so `npm ci` keeps working unchanged.

## Packaging

- `asciiverse/build.sh`: the release build with `bun build --compile`,
  one executable holding the Bun runtime, the game and its libraries.
  Bun was chosen over Node's single executable applications because it
  builds for Linux, macOS and Windows alike from the ES modules Ink needs
  (with top-level await, which Node's single executables do not take). It
  changes one line of `node_modules/yoga-wasm-web/dist/node.js` before
  bundling, so Ink's layout engine imports `yoga.wasm` (embedded by Bun)
  instead of reading it from disk; it fails if that line ever changes.
- `.github/workflows/asciiverse-release.yml`: builds Linux x86-64 and
  ARM64, macOS Apple silicon and Intel, and Windows x86-64, smoke-tests
  Linux and macOS Apple silicon, and attaches archives and SHA256SUMS to
  the release. Upstream's own workflows (CI, and npm publishing from
  `master`) are left as they are; they never run on the `asciiverse`
  branch.
- `asciiverse/smoke.py`: the smoke test (80x32, empty HOME, scratch
  `XDG_STATE_HOME`, checks that nothing is written).
- `asciiverse/record-preview.sh`, `asciiverse/drive.py`: record the
  100x30 preview, a scripted first trade, in a tmux pane.
- `asciiverse/README.md`: the package README, shipped in the archive.
- `asciiverse/sea-trader.toml`, `.md`, `.cast`: the catalog manifest,
  store page and 100x30 preview, drafts for `hub/catalog`.

## Not changed

- No session log: the game is React components and an XState machine, and
  a log would mean wiring a file writer through upstream's plugin hooks,
  which is game code, not packaging.
