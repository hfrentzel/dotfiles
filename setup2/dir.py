import os
from operator import itemgetter
from .job import Job

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
    out = ""
    out += 'SUB-DIRECTORIES\n'
    for dir in sorted(desired_dirs, key=itemgetter('path')):
        out += f'{dir["path"]}\n'

    return out

async def get_statuses():
    tasks = []
    for dir in desired_dirs:
        check_results.append(check_job(dir))

def status_printout(show_all):
    out = ""
    for dir in sorted(check_results, key=itemgetter('path')):
        if not show_all and dir['complete']:
            continue
        out += f"{dir['path']: <18} {dir['status']: <13}\n"

    return 'SUB-DIRECTORIES    STATUS\n' + out if out != "" else ""

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
                job=create_directory(dir['path'])
            )
    
    return no_action_needed, jobs

def create_directory(path):
    async def inner():
        full_path = os.path.expanduser(path)
        os.makedirs(full_path)

        return True

    return inner
