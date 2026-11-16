"""smoke.py SEA_TRADER_BINARY: start the game in an 80x32 pseudo-terminal
from another directory, with an empty HOME and a scratch XDG_STATE_HOME,
start a voyage from the start screen, quit with Esc, and fail unless the
start screen and the first day in Hong Kong were drawn. The game keeps
nothing on disk, so it also fails if anything was written to HOME or
XDG_STATE_HOME."""
import fcntl, os, pty, re, select, signal, struct, sys, tempfile, termios, time

binary = os.path.abspath(sys.argv[1])
home = tempfile.mkdtemp()
state = tempfile.mkdtemp()
os.chdir(tempfile.mkdtemp())
pid, fd = pty.fork()
if pid == 0:
    os.environ.clear()
    os.environ.update(TERM="xterm-256color", HOME=home, XDG_STATE_HOME=state,
                      PATH="/usr/bin:/bin", LANG="C.UTF-8")
    os.execv(binary, [binary])
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 32, 80, 0, 0))

def read_for(seconds):
    out, end = b"", time.time() + seconds
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try:
                out += os.read(fd, 65536)
            except OSError:
                break
    return out

def plain(data):
    text = data.decode("utf-8", "replace")
    return re.sub(r"\x1b\[[0-9;?<>]*[ -/]*[@-~]|\x1b[()][0-9A-Za-z]|\x1b[=>78]", "", text)

start = read_for(4)
os.write(fd, b"\r")
game = read_for(3)
os.write(fd, b"\x1b")
read_for(1)
os.kill(pid, signal.SIGKILL)
print(f"{len(start)} + {len(game)} bytes of output")
if "The year is 1850" not in plain(start):
    print(plain(start)[-2000:])
    sys.exit("smoke test failed: the start screen was not drawn")
if "Hong Kong" not in plain(game):
    print(plain(game)[-2000:])
    sys.exit("smoke test failed: the voyage did not start in Hong Kong")
left = [os.path.join(d, f) for top in (home, state) for d, _, fs in os.walk(top) for f in fs]
if left:
    sys.exit(f"smoke test failed: files written: {left}")
print("ok: the start screen and the first day in Hong Kong were drawn, nothing written")
