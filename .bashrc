#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

PS1="\[\e[36m\]\u\[\e[0m\]\[\e[37m\]:\[\e[0m\]\[\e[33m\]\w\[\e[0m\] \[\e[32m\]\$\[\e[0m\] "
export PATH="$PATH:/home/idefa/.local/bin"
