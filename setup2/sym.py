import os
from operator import itemgetter
from .job import Job
from .conf import conf
from .output import print_grid


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
    lines = []
    for sym in sorted(desired_syms, key=itemgetter('target')):
        lines.append((sym['target'],))
    return print_grid(('SYMLINKED FILES',), lines)


async def get_statuses():
    tasks = []
    for sym in desired_syms:
        check_results.append(check_job(sym))


def status_printout(show_all):
    lines = []
    for sym in sorted(check_results, key=itemgetter('name')):
        if not show_all and sym['complete']:
            continue
        lines.append((sym['name'], sym['status']))
    return print_grid(('SYMLINK', 'STATUS'), lines)

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
                description=f'Generate symlink at {sym["target"]}',
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
