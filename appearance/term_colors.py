#! /usr/bin/env python
# color.py
# This is an implementation of base16 colorscheming for a terminal environment
# using themes from https://github.com/tinted-theming/schemes and based on the
# scripts from https://github.com/chriskempson/base16-shell. The script works by
# modifying the rgb values of the terminals default 16-color palette.
import os
import shlex
import subprocess
import sys

scheme_dir = os.path.expanduser("~/dotfiles/appearance/schemes/base16/")
scheme_dir_24 = os.path.expanduser("~/dotfiles/appearance/schemes/base24/")
save_file = os.path.expanduser("~/.local/share/mysetup/base16")

if os.environ.get("TMUX"):

    def apply_color(number, rgb):
        x = f"{rgb[0:2]}/{rgb[2:4]}/{rgb[4:6]}"
        print(f"\033Ptmux;\033\033]4;{number};rgb:{x}\033\033\\\033\\", end="")

    def apply_color_var(number, rgb):
        x = f"{rgb[0:2]}/{rgb[2:4]}/{rgb[4:6]}"
        print(f"\033Ptmux;\033\033]{number};rgb:{x}\033\033\\\033\\", end="")

else:

    def apply_color(number, rgb):
        x = f"{rgb[0:2]}/{rgb[2:4]}/{rgb[4:6]}"
        print(f"\033]4;{number};rgb:{x}\033\\", end="")

    def apply_color_var(number, rgb):
        x = f"{rgb[0:2]}/{rgb[2:4]}/{rgb[4:6]}"
        print(f"\033]{number};rgb:{x}\033\\", end="")


def set_color(scheme):
    is_24 = False

    if os.path.exists(f"{scheme_dir_24}{scheme}.yaml"):
        scheme_file = f"{scheme_dir_24}{scheme}.yaml"
        is_24 = True
    else:
        scheme_file = f"{scheme_dir}{scheme}.yaml"

    colors = {}
    try:
        with open(scheme_file, encoding="utf-8") as f:
            for line in f.readlines():
                if line.startswith("  base"):
                    colors[line[6:8]] = line[12:18]
    except FileNotFoundError:
        print(f"Bad colorscheme {scheme}")
        return

    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    if len(sys.argv) < 3 or sys.argv[2] != "--no-save":
        with open(save_file, "w") as c:
            c.write(scheme)

    apply_color(0, colors["00"])  # Black
    apply_color(1, colors["08"])  # Red
    apply_color(2, colors["0B"])  # Green
    apply_color(3, colors["0A"])  # Yellow
    apply_color(4, colors["0D"])  # Blue
    apply_color(5, colors["0E"])  # Magenta
    apply_color(6, colors["0C"])  # Cyan
    apply_color(7, colors["05"])  # White
    apply_color(8, colors["03"])  # Bright Black
    apply_color(9, colors["12"] if is_24 else colors["08"])
    apply_color(10, colors["14"] if is_24 else colors["0B"])
    apply_color(11, colors["13"] if is_24 else colors["0A"])
    apply_color(12, colors["16"] if is_24 else colors["0D"])
    apply_color(13, colors["17"] if is_24 else colors["0E"])
    apply_color(14, colors["15"] if is_24 else colors["0C"])
    apply_color(15, colors["07"])
    apply_color(16, colors["09"])
    apply_color(17, colors["0F"])
    apply_color(18, colors["01"])
    apply_color(19, colors["02"])
    apply_color(20, colors["04"])
    apply_color(21, colors["06"])

    apply_color_var(10, colors["05"])
    apply_color_var(11, colors["00"])

    if os.environ.get("TMUX"):
        subprocess.run(
            shlex.split(f"tmux set -a window-active-style bg=#{colors['00']}")
        )
        subprocess.run(
            shlex.split(f"tmux set -a window-style bg=#{colors['01']}")
        )
        subprocess.run(
            shlex.split(
                f"tmux set -a pane-active-border-style bg=#{colors['01']}"
            )
        )
        subprocess.run(
            shlex.split(f"tmux set -a pane-border-style bg=#{colors['01']}")
        )


def print_current():
    with open(save_file, encoding="utf-8") as f:
        print(f.read())


def color_picker():
    schemes = set(os.listdir(scheme_dir) + os.listdir(scheme_dir_24))
    schemes = sorted({s.removesuffix(".yaml") for s in schemes})
    schemes_str = "\n".join(schemes)

    with open(save_file, encoding="utf-8") as f:
        current_scheme = f.read()

    curr_pos = schemes.index(current_scheme)
    cmd = (
        f"fzf --bind 'load:pos({curr_pos + 1}),"
        "enter:execute(color {})+accept,"
        "focus:execute(color {} --no-save),"
        f"esc:execute(color {current_scheme})+abort'"
    )

    subprocess.run(
        shlex.split(cmd),
        input=bytes(schemes_str, encoding="utf-8"),
    )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        color_picker()
        sys.exit()
    scheme = sys.argv[1]

    if scheme == "--current":
        print_current()
    else:
        set_color(scheme)
