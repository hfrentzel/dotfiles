import os
from operator import itemgetter
from .job import Job
from .output import print_grid

desired_dirs = []
check_results = []

def Dir(name, path):
    desired_dirs.append(
        {
            "name": name,
            "path": path
        }
    )

def check_job(dir):
    path = os.path.expanduser(dir['path'])
    if os.path.isdir(path):
        return {
            **dir,
            'complete': True,
            'status': 'EXISTS'
        }
    elif os.path.exists(path):
        return {
            **dir,
            'complete': False,
            'status': 'BLOCKED'
        }
    else:
        return {
            **dir,
            'complete': False,
            'status': 'MISSING'
        }

def desired_printout():
    lines = []
    for dir in sorted(desired_dirs, key=itemgetter('path')):
        lines.append((dir['path'],))
    return print_grid(('SUB-DIRECTORIES',), lines)

async def get_statuses():
    tasks = []
    for dir in desired_dirs:
        check_results.append(check_job(dir))

def status_printout(show_all):
    lines = []
    for dir in sorted(check_results, key=itemgetter('path')):
        if not show_all and dir['complete']:
            continue
        lines.append((dir['path'], dir['status']))
    return print_grid(('SUB-DIRECTORIES', 'STATUS'), lines)

def create_jobs():
    no_action_needed = []
    jobs = {}
    for dir in check_results:
        if dir['complete']:
            no_action_needed.append(dir['name'])
        elif dir['status'] == 'BLOCKED':
            #TODO Add unblocking job
            pass
        else:
            jobs[dir['name']] = Job(
                names=[dir['name']],
                description=f'Create directory at {dir["path"]}',
                job=create_directory(dir['path'])
            )
    
    return no_action_needed, jobs

def create_directory(path):
    async def inner():
        full_path = os.path.expanduser(path)
        os.makedirs(full_path)

        return True

    return inner
