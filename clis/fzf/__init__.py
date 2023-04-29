import os
from setup_tools.managers import Tar, Symlink
from setup_tools.jobs import add_job
from setup_tools.installers import async_proc

def fzf():
    Tar(command='fzf', version='0.39.0',
        includes='bin',
        url='https://github.com/junegunn/fzf/releases/download/'
            '{version}/fzf-{version}-linux_amd64.tar.gz',
        )

    async def fzf_completion():
        # Add fzf completion file
        completion_file = '~/.local/shell/fzf.sh'
        if not os.path.isfile(completion_file):
            os.makedirs('~/.local/shell', exist_ok=True)
            print('Downloading fzf completion script')
            await async_proc(
                'curl -s https://raw.githubusercontent.com/'
                'junegunn/fzf/0.39.0/shell/completion.bash '
                f'-o {completion_file}')
        return True
    add_job(fzf_completion())

    Symlink('DOTROOT/clis/fzf/fzf.sh', '~/.config/fzf/fzf.bash')
