#! /usr/bin/env python
import os
import platform
import shlex
import subprocess
import sys

if platform.system() == "Linux":
    if os.path.isfile("/proc/sys/fs/binfmt_misc/WSLInterop"):
        subprocess.run(
            ["clip.exe"],
            stdin=sys.stdin,
            encoding="utf_16le",
        )
    else:
        subprocess.run(
            shlex.split("xclip -sel clipboard"),
            stdin=sys.stdin,
            capture_output=True,
        )
else:
    subprocess.run(["clip.exe"], stdin=sys.stdin, encoding="utf_16le")
