#!/usr/bin/zsh
xset +fp /usr/share/fonts/local
xset fp rehash
xset -b # disable bell
eval `/usr/bin/ssh-agent`
if test -f /usr/lib/openssh/x11-ssh-askpass
then
	SSH_ASKPASS=/usr/lib/openssh/x11-ssh-askpass ssh-add < /dev/null
fi
xrdb -merge $HOME/.Xresources
xmodmap ~/.Xmodmap
setxkbmap -layout us -option ctrl:nocaps
while true
do
	VOL=$(amixer get Master | tail -1 | sed 's/.*\[\([0-9]*%\)\].*/\1/')
	LOCALTIME=$(date +%Z\=%Y-%m-%dT%H:%M)
	IP=$(for i in `ip r`; do echo $i; done | grep -A 1 src | tail -n1)
	TEMP="$(($(cat /sys/class/thermal/thermal_zone0/temp) / 1000))C"
	if acpi -a | grep off-line > /dev/null
	then
		BAT="Bat. $(acpi -b | awk '{ print $4 " " $5 }' | tr -d ',')"
		xsetroot -name "$IP $BAT $VOL $TEMP $LOCALTIME"
	else
		xsetroot -name "$IP $VOL $TEMP $LOCALTIME"
	fi
	sleep 20s
done &
exec dwm