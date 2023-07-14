import argparse
import asyncio

from .exe import Exe, exe_desired_printout, exe_status_printout
from .sym import Sym, sym_desired_printout, sym_status_printout

def show_desired(symlinks_only):
    print(sym_desired_printout(), end="")
    if symlinks_only:
        return
    print(exe_desired_printout(), end="")

async def show_current_status(show_all):
    print(sym_status_printout(show_all), end="")
    print(await exe_status_printout(show_all), end="")

def run():
    parser = argparse.ArgumentParser( prog = 'EnvSetup')
    parser.add_argument('--show-all', action='store_true')
    parser.add_argument('--show-desired', action='store_true')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--symlinks-only', action='store_true')
    args = parser.parse_args()

    if args.show_desired:
        show_desired(args.symlinks_only)
    elif args.status:
        asyncio.run(show_current_status(args.show_all))
