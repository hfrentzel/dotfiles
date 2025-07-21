# This is a utility script meant to be used by the setup submodules resource
# to check whether any git submodules are out of date. It does this by running
# `git submodule status` and then looking for any `+` or `~` markers on the
# output.
import subprocess
import sys

result = subprocess.run(["git", "submodule", "status"], capture_output=True)

lines = result.stdout.decode().rstrip().split("\n")

if any(not line.startswith(" ") for line in lines):
    sys.exit(1)
else:
    sys.exit(0)
