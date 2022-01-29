
first_tmux_session() {
    tmux \
    new-session -d -n "nvim" \
        ~/.config/sxhkd/nvim-forever.sh ';' \
    attach ';' \
    new-window ~/.config/sxhkd/zsh-forever.sh
}

while true
do
    export LANG="en_US.UTF-8"
    tmux attach || first_tmux_session
done
