"""Plays Sea Trader for the catalog preview (asciiverse/record-preview.sh).

Reads the tmux pane and presses keys at a watchable pace: a look at the
start screen, then a first trade. In the Hong Kong market it buys as much
of the good (opium left aside) with the best price gap as the money allows, sails to the
port that pays most for it, answers whatever the sea brings on the way
(the first choice of an event, attack for pirates, Space for the crew's
reports), sells everything there, looks in at the shipyard and quits.
    python3 -I drive.py <tmux socket> <session> [debug]
"""
import re
import subprocess
import sys
import time

SOCK, SESS = sys.argv[1], sys.argv[2]
DEBUG = len(sys.argv) > 3
T0 = time.time()
GOODS = ["Wheat", "Tea", "Spices", "Opium", "Porcelain"]
PORTS = ["Hong Kong", "Shanghai", "Nagasaki", "Singapore", "Manila"]


def tmux(*args):
    return subprocess.run(["tmux", "-L", SOCK, *args], capture_output=True,
                          text=True).stdout


def screen():
    return tmux("capture-pane", "-p", "-t", SESS)


def key(k, wait=1.2):
    if DEBUG:
        print(round(time.time() - T0, 1), repr(k), file=sys.stderr)
    tmux("send-keys", "-t", SESS, k)
    time.sleep(wait)


def typed(text):
    for ch in text:
        key(ch, 0.35)
    time.sleep(0.6)
    key("Enter", 1.5)


def wait_for(text, seconds=10):
    end = time.time() + seconds
    while time.time() < end:
        if text in screen():
            return True
        time.sleep(0.2)
    if DEBUG:
        print("did not see", text, file=sys.stderr)
    return False


def prices(s):
    table = {}
    for port in PORTS:
        m = re.search(re.escape(port) + r"((?:\s+\$\d+){5})", s)
        if m:
            table[port] = [int(x) for x in re.findall(r"\d+", m.group(1))]
    return table


wait_for("The year is 1850")
time.sleep(3.5)
key("Enter", 2)
wait_for("What would you like to do")
time.sleep(1)
key("2", 2.5)                                  # Visit Market
table = prices(screen())
here = table.get("Hong Kong", [1] * 5)
best = max((0, 1, 2, 4), key=lambda g: max(table[p][g] for p in PORTS[1:] if p in table) / here[g]
           if here[g] * 2 < 1500 else 0)
dest = max(PORTS[1:], key=lambda p: table.get(p, [0] * 5)[best])
key("1", 1.2)                                  # Buy Goods
key(str(best + 1), 1.5)
m = re.search(r"buy up to (\d+) picul", screen())
typed(m.group(1) if m else "1")
wait_for("Press [SPACE]")
time.sleep(1.5)
key("Space")
key("Escape")
key("Escape", 1.5)                             # main menu
key("1", 2.5)                                  # Go to Port
key(str(PORTS[1:].index(dest) + 1), 1)
end = time.time() + 60
while time.time() < end:
    s = screen()
    if "Arrived at" in s:
        time.sleep(1.5)
        key("Space", 1.5)
        break
    if "Attack them" in s:
        time.sleep(1.5)
        key("1", 1.5)
    elif re.search(r"EVENT", s) and "[1]" in s:
        time.sleep(2)
        key("1", 1.5)
    elif "Press [SPACE]" in s:
        time.sleep(2)
        key("Space", 1.2)
    else:
        time.sleep(0.3)
wait_for("What would you like to do")
key("2", 2)                                    # Visit Market
key("2", 1.2)                                  # Sell Goods
key(str(best + 1), 1.5)
m = re.search(r"In Hold((?:\s+\d+){5})", screen())
held = re.findall(r"\d+", m.group(1))[best] if m else "1"
typed(held)
wait_for("Press [SPACE]")
time.sleep(2.5)
key("Space")
key("Escape")
key("Escape", 1.5)
key("3", 4)                                    # Visit Shipyard
key("Escape", 1.5)
key("Escape", 1.5)
key("y", 1.5)
