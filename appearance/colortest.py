#! /usr/bin/env python
import os
import sys

scheme = sys.argv[1]
scheme_dir = os.path.expanduser("~/dotfiles/appearance/schemes/base16/")
scheme_dir_24 = os.path.expanduser("~/dotfiles/appearance/schemes/base24/")
save_file = os.path.expanduser("~/.local/share/mysetup/base16")
is_24 = False

if os.path.exists(f"{scheme_dir_24}{scheme}.yaml"):
    scheme_file = f"{scheme_dir_24}{scheme}.yaml"
else:
    scheme_file = f"{scheme_dir}{scheme}.yaml"

colors = {}
with open(scheme_file, encoding="utf-8") as f:
    for line in f.readlines():
        if line.startswith("  base"):
            colors[line[6:8]] = line[12:18]


for key, color in colors.items():
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    print(f"{key}: \033[48;2;{r};{g};{b}m                      ", end="")
    print("\033[0m")
