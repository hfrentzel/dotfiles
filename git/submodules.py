import subprocess
import shlex


def check_submodules():
    print('Fetcing submodules')
    subprocess.run(shlex.split('git submodule foreach git fetch'),
                   capture_output=True)

    cmd = "git submodule --quiet foreach " \
          "'echo ${PWD##*/}; " \
          "git show -s --format=%ci; " \
          "git rev-list --count `git rev-parse --abbrev-ref HEAD`" \
          "..`git rev-parse --abbrev-ref origin/HEAD`'"

    result = subprocess.run(shlex.split(cmd), capture_output=True)

    lines = result.stdout.decode().split('\n')

    data = list(zip(*[iter(lines)]*3))
    data.sort(key=lambda x: (int(x[2]) == 0, x[1]), reverse=True)

    max_len = max(len(d[0]) for d in data)

    for d in data:
        date = d[1].split(' ')[0]
        commits_behind = int(d[2])
        if commits_behind == 0:
            behind_statement = 'Up to Date'
        else:
            behind_statement = f'{commits_behind: <3} commits_behind'

        print(f'{d[0]: <{max_len}}  Last Updated: {date}, '
              f'{behind_statement}')


if __name__ == '__main__':
    check_submodules()
