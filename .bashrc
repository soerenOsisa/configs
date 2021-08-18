alias s6e='s6-rc-bundle-update -c /etc/s6/rc/compiled add default'
alias s6u='s6-rc -u change'
alias s6d='s6-rc -d change'
alias pac='pacman --noconfirm -S'
alias pacu='pacman --noconfirm -Syu'
alias aur='sh /usr/local/bin/aur'
alias gitc='git clone https://github.com/'
s6-rc -u change elogind
s6-rc -u change iwd
s6-rc -u change dhcpcd