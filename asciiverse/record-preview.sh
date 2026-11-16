#!/bin/sh
# Records the 100x30 catalog preview, asciiverse/sea-trader.cast
# (hub/RECORDING.md): the start screen, then a first trade out of Hong
# Kong to the port that pays most, whatever the sea brings on the way,
# the sale, a look at the shipyard, and quitting, played by
# asciiverse/drive.py. asciinema records a tmux pane (own socket, no
# status line, no user config) that drive.py reads and plays into. Needs
# asciinema 3 and tmux.
#   asciiverse/record-preview.sh ./sea-trader       # the release executable
#   asciiverse/record-preview.sh dist/cli.js        # or upstream's Node build
set -eu
game=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
here=$(cd "$(dirname "$0")" && pwd)
out=$here/sea-trader.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir "$home/bin"
case "$game" in
  *.js) printf '#!/bin/sh\nexec node "%s"\n' "$game" > "$home/bin/sea-trader"; chmod +x "$home/bin/sea-trader" ;;
  *) cp "$game" "$home/bin/sea-trader" ;;
esac
cd "$home"  # nothing in the recording names a local path
export HOME="$home" XDG_STATE_HOME="$home/state" \
  PATH="$home/bin:$PATH" USER=player LOGNAME=player \
  TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
unset CI
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 "sea-trader" \; set -g status off
python3 -I "$here/drive.py" avrec rec ${DEBUG:+debug} &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "Sea Trader" \
  --command "tmux -L avrec attach -t rec" "$out"
wait "$drive"
