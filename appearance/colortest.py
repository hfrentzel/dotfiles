#! /usr/bin/env python
import os
import sys

scheme = sys.argv[1]
scheme_dir = os.path.expanduser("~/dotfiles/appearance/schemes/base16/")

colors = {}
with open(f"{scheme_dir}{scheme}.yaml", encoding="utf-8") as f:
    for line in f.readlines():
        if line.startswith("  base"):
            colors[line[6:8]] = line[12:18]


for key, color in colors.items():
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    print(f"{key}: \033[48;2;{r};{g};{b}m                      ", end="")
    print("\033[0m")
