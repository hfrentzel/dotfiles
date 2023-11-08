import atexit
import os
import sys
import readline

try:
    readline.parse_and_bind("tab: complete")
except ImportError:
    pass

if hasattr(sys, '__interactivehook__'):
    del sys.__interactivehook__

histfile = os.path.join(os.path.expanduser("~"), ".local/share/python/history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

sys.ps1 = f'py{sys.version_info[0]}.{sys.version_info[1]}> '
sys.ps2 = '.' * (len(sys.ps1) - 1) + ' '

class Quitter:
    def __init__(self, num=0):
        self.num = num

    def __repr__(self):
        sys.exit(self.num)


ch = Quitter(5)
q = Quitter()
exit = q
