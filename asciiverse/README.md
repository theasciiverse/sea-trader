# Sea Trader

**The year is 1850. You have a small junk, $1500 and 200 days.**

Hong Kong harbour, the first morning of the voyage. Shanghai grows its
own tea and sells it cheap, porcelain is cheap in Nagasaki where the kilns are,
and Manila sells its own spices below anyone else. Somewhere between them
are storms, typhoons, reefs, uncharted islands with buried chests, and
pirates who want your hold more than your life. Buy where it is cheap,
sell where it is dear, and come home on day 200 a Captain, or an Admiral.

Sea Trader is Yishai Zehavi's trading voyage through the South China Sea
and beyond: five ports from Singapore to Nagasaki, prices that move every
fourteen days and swing with the seasons, merchant tips that get better as
your reputation grows, and a shipyard where the junk grows faster, tougher
and roomier, with guard ships to hire against the pirates. Overload the
hold by a fifth if you dare, and sail slower for it. Fall into debt and
the moneylenders take 3% a day.

## Playing

Run `sea-trader` in a terminal of at least 60x20; at 80x32 every screen
fits whole.

- **Number keys** pick an option, or **arrow keys** and **Enter** (press
  **C** on the start screen to switch)
- **Space**: continue after a report from the crew
- **Esc**: back; on the main menu it asks whether to quit
- **PgUp** / **PgDn** or the mouse wheel: scroll a long screen
- On the start screen: **H** how to play, **M** classic or extended
  voyage, **A** text animations on or off

A voyage lasts one sitting: Sea Trader keeps nothing on disk.

## Credits

- Sea Trader: Yishai Zehavi (zyishai), https://github.com/zyishai/sea-trader
  (MIT, see LICENSE)
- Built with Ink, XState and figlet.js
- This package: Asciiverse, for the av launcher and the catalog at
  https://asciiverse.sh. What we changed is in PATCHES.md, and what
  changed in the game is in CHANGELOG.md.

## Building

`npm ci --ignore-scripts`, then `sh asciiverse/build.sh` with Bun 1.2,
makes `stage/sea-trader`, one executable with the Bun runtime inside; the
release workflow (`.github/workflows/asciiverse-release.yml`) builds it for
Linux, macOS and Windows. Upstream's own way, `npm install` and
`npm run dev`, runs it on Node.
