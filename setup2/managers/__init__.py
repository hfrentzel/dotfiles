from typing import Dict
from setup2.conf import conf
from setup2.job import Job
from .directory import Dir
from .exe_class import Exe
from .exe import create_bonus_jobs
from .sym import Sym
from .lib import Lib
from .command import Command
from .parser import Parser

__all__ = ['Dir', 'Exe', 'Sym', 'Lib', 'Command', 'Parser']


def create_jobs() -> Dict[str, Job]:
    jobs = {}
    for t in conf.types:
        for resource, complete, status in t.check_results:
            if complete:
                continue
            if status == 'BLOCKED':
                # TODO Add unblocking job
                pass
            else:
                job = t.create_job(resource)
                if job is not None:
                    jobs[resource.name] = job
    jobs.update(create_bonus_jobs())
    return jobs
