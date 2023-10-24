import os
from operator import itemgetter
from .job import Job
from .conf import conf


desired_syms = []
check_results = []

def Sym(name, source, target):
    desired_syms.append(
        {
            "name": name,
            "source": source,
            "target": target
        }
    )

def check_job(sym):
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

def desired_printout():
    out = ""
    out += 'SYMLINKED FILES\n'
    for sym in sorted(desired_syms, key=itemgetter('target')):
        out += f'{sym["target"]}\n'

    return out


async def get_statuses():
    tasks = []
    for sym in desired_syms:
        check_results.append(check_job(sym))


def status_printout(show_all):
    out = ""
    for sym in sorted(check_results, key=itemgetter('name')):
        if not show_all and sym['complete']:
            continue
        out += f"{sym['name']: <13} {sym['status']: <13}\n"

    return 'SYMLINK       STATUS\n' + out if out != "" else ""

def create_jobs():
    no_action_needed = []
    jobs = {}
    for sym in check_results:
        if sym['complete']:
            no_action_needed.append(sym['name'])
        elif sym['status'] == 'BLOCKED':
            #TODO Add unblocking job
            pass
        else:
            jobs[sym['name']] = Job(
                names=[sym['name']],
                job=create_symlink(sym['source'], sym['target'])
            )
    
    return no_action_needed, jobs

def create_symlink(source, target):
    async def inner():
        src = source.replace('DOT', conf.dotfiles_home)
        src = os.path.expanduser(src)
        dest = os.path.expanduser(target)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.symlink(src, dest)

        return True

    return inner
