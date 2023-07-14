import os
from operator import itemgetter


syms = []
def Sym(name, source, target):
    syms.append(
        {
            "name": name,
            "source": source,
            "target": target
        }
    )

def sym_check_job(sym):
    src = os.path.expanduser(sym['source'])
    dest = os.path.expanduser(sym['target'])
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            return {
                **sym,
                'complete': True,
                'status': 'LINKED'
            }
        return {
            **sym,
            'complete': False,
            'status': 'BLOCKED'
        }

    return {
        **sym,
        'complete': False,
        'status': 'MISSING'
    }

def sym_desired_printout():
    out = ""
    out += 'SYMLINKED FILES\n'
    for sym in syms:
        out += f'{sym["target"]}\n'

    return out


def sym_status_printout(show_all):
    results = []
    tasks = []
    for sym in syms:
        results.append(sym_check_job(sym))

    out = ""
    for sym in sorted(results, key=itemgetter('name')):
        if not show_all and sym['complete']:
            continue
        out += f"{sym['name']: <13} {sym['status']: <13}\n"

    if out != "":
        return 'SYMLINK       STATUS\n' + out
    else:
        return ""
