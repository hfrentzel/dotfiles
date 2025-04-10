import contextlib
import os
import platform
import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import Iterator
from io import TextIOWrapper

WINDOWS = platform.system() == "Windows"

if WINDOWS:
    import msvcrt
else:
    import termios


class MenuPiece(ABC):
    @abstractmethod
    def get(self, index: int) -> str:
        pass

    @abstractmethod
    def len(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def keys() -> list[str]:
        pass

    @abstractmethod
    def action(self, key: str, index: int) -> bool:
        pass


class XX:
    def __init__(self, size: int = 0):
        self.size = size

    @contextlib.contextmanager
    def tty_handler(self) -> Iterator[tuple[TextIOWrapper, TextIOWrapper]]:
        if WINDOWS:
            tty_in = open(sys.stdin.fileno(), encoding="utf-8")
            tty_out = open(sys.stdout.fileno(), "w", encoding="utf-8")
        else:
            tty_in = open("/dev/tty", encoding="utf-8")
            tty_out = open("/dev/tty", "w", encoding="utf-8", errors="replace")
            old_term = termios.tcgetattr(tty_in.fileno())
            new_term = termios.tcgetattr(tty_in.fileno())
            new_term[3] = new_term[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(tty_in.fileno(), termios.TCSAFLUSH, new_term)

            # Enter terminal application mode to get expected escape codes
            # for arrow keys
            tty_out.write(TERM_COMMAND["enter_application_mode"])
        tty_out.write(TERM_COMMAND["cursor_invisible"])
        try:
            yield tty_in, tty_out
        except KeyboardInterrupt:
            pass
        finally:
            tty_out.write(self.size * TERM_COMMAND["delete_line"])
            tty_out.flush()
            if not WINDOWS:
                termios.tcsetattr(tty_out.fileno(), termios.TCSAFLUSH, old_term)
            tty_out.write(TERM_COMMAND["cursor_visible"])
            if not WINDOWS:
                tty_out.write(TERM_COMMAND["exit_application_mode"])
            tty_in.close()
            tty_out.close()


CAP_TO_ANSI = {
    "clear_to_end_of_line": "\033[K",
    "cursor_down": "\033[1B",
    "cursor_invisible": "\033[?25l",
    "cursor_up": "\033[1A",
    "cursor_visible": "\033[?25h",
    "delete_line": "\033[1M",
    "down": "\033[B",
    "enter_application_mode": "",
    "exit_application_mode": "",
    "up": "\033[A",
}


def query_terminfo_database(capname: str) -> str:
    return subprocess.check_output(["tput", capname], universal_newlines=True)


CODENAME_TO_CAPNAME = {
    "clear_to_end_of_line": "el",
    "cursor_down": "cud1",
    "cursor_invisible": "civis",
    "cursor_up": "cuu1",
    "cursor_visible": "cnorm",
    "delete_line": "dl1",
    "down": "kcud1",
    "enter_application_mode": "smkx",
    "exit_application_mode": "rmkx",
    "up": "kcuu1",
}
TERM_COMMAND = {
    codename: query_terminfo_database(capname)
    if not WINDOWS
    else CAP_TO_ANSI[codename]
    for codename, capname in CODENAME_TO_CAPNAME.items()
}
TERM_COMMAND.update({"enter": "\015" if WINDOWS else "\012", "escape": "\033"})
DECODE_RAW_INPUT = {
    terminal_code: codename for codename, terminal_code in TERM_COMMAND.items()
}


def read_input(tty: TextIOWrapper) -> str:
    if WINDOWS:
        code = "\xe0"
        while code in {"\xe0", "\x00"}:
            code = msvcrt.getch().decode("ascii", errors="ignore")
    else:
        code = os.read(tty.fileno(), 80).decode("ascii", errors="ignore")
    next_key = DECODE_RAW_INPUT.get(code, code)
    return next_key


def show(menu_options: MenuPiece) -> int:
    active_index = 0
    x = XX(menu_options.len())
    with x.tty_handler() as (tin, tout):
        while True:
            for menu_index in range(menu_options.len()):
                tout.write("* " if menu_index == active_index else "  ")
                tout.write(menu_options.get(menu_index))
                tout.write(TERM_COMMAND["clear_to_end_of_line"])
                if menu_index < menu_options.len() - 1:
                    tout.write("\n")

            tout.write(
                "\r" + (menu_options.len() - 1) * TERM_COMMAND["cursor_up"]
            )
            tout.flush()
            next_key = read_input(tin)
            if next_key in {"up", "k"}:
                active_index = max(0, active_index - 1)
            elif next_key in {"down", "j"}:
                active_index = min(menu_options.len() - 1, active_index + 1)
            elif next_key in menu_options.keys():
                if menu_options.action(next_key, active_index):
                    break
            elif next_key in {"escape", "q", "ctrl-g"}:
                active_index = -1
                break

    return active_index
