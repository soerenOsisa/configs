#!/bin/bash
[ -f ~/.fehbg ] && sh ~/.fehbg &
[ ! -f ~/.fehbg ] && feh --bg-scale /usr/local/boot.png

urxvtd -q -o -f

while true; do
    xsetroot -name "$(iwconfig wlan0 | sed 's/ /\n/g' | grep ESSID) | $(iwconfig wlan0 | sed 's/ /\n/g' | grep Quality) | $(uptime | sed 's/.*://; s/,//g') | $(date "+%F %R") |"
    sleep 1m
done &

exec dwm
exec dwm