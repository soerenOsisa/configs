alias s-e='s6-rc-bundle-update add default'
alias s-u='s6-rc -u change'
alias s-d='s6-rc -d change'
alias pac='pacman --noconfirm -S'
alias aur='sh /usr/local/bin/aur.sh'
alias gitc='git clone https://github.com/'
s6-rc -u change elogind
s6-rc -u change iwd
s6-rc -u change dhcpcd

startx