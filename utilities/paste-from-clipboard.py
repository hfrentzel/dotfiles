#! /usr/bin/env python
import os
import platform
import shlex
import subprocess

if platform.system() == "Linux":
    if os.path.isfile("/proc/sys/fs/binfmt_misc/WSLInterop"):
        output = subprocess.run(
            shlex.split("powershell.exe -c Get-Clipboard"), capture_output=True
        ).stdout
        print(output.decode().replace("\r\n", "\n")[:-1], end="")
    else:
        print(
            subprocess.run(
                shlex.split("xclip -out -sel clipboard"),
                capture_output=True,
            ).stdout.decode()
        )
else:
    output = subprocess.run(
        shlex.split("powershell.exe -c Get-Clipboard"), capture_output=True
    ).stdout
    print(output.decode().replace("\r\n", "\n")[:-1], end="")
