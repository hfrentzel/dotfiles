from setup2 import Exe, Sym, Command


def fzf():
    Exe('fzf', '0.39.0', installers=['Github'], repo='junegunn/fzf')
    Command('fzf_completion',
            cwd='~/.local',
            check_script='test -f shell/fzf.sh',
            run_script='mkdir -p shell; curl -s https://raw.githubusercontent.com/'
                'junegunn/fzf/0.39.0/shell/completion.bash -o shell/fzf.sh')

    Sym('fzf_setup', 'DOT/clis/fzf/fzf.sh', '~/.config/fzf/fzf.bash')
