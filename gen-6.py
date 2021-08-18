#pacman --noconfirm -Sy git && git clone https://github.com/soerenOsisa/configs && sh configs/6
inp = input("Options: ").split(",")
args = [x.split(" ") for x in inp]
keys = [q[0] for q in args]
vals = [q[1] for q in args]
options = dict(zip(keys,vals))

try: drive = '{}"'.format(options['d']);
except: drive = "\"$(lsblk -S | awk {'print $1'} | sed -n '2 p')";
try: boot = str(2048*int(options['b']));
except: boot = "524288";
try: user = options['u'];
except: user = "nair";
try: passwd = options['p'];
except: passwd = "nair";
try: hostname = options['h'];
except: hostname = "nair";
try: timez = options['t'];
except: timez = "UTC";
try:
	i = args[-1].index('i')
	packages = args[-1][1:]
	install = "pacman --noconfirm -S " + ' '.join(packages);
except: install = "";

s6 = '''
#!/bin/bash
drive="/dev/{}
#DRIVE
sfdisk $drive -f -w auto -X dos << EOF
,{},L,*
;
EOF
mkfs.fat -F32 $drive"1"
mkfs.ext4 $drive"2"
mount $drive"2" /mnt
mkdir /mnt/boot
mount $drive"1" /mnt/boot
#BASE
basestrap /mnt base base-devel s6-base elogind-s6 linux-zen linux-firmware
fstabgen -U /mnt >> /mnt/etc/fstab
modprobe efivarfs
artix-chroot /mnt | sh configs/62
umount -R /mnt
reboot
'''.format(drive,boot)
s62='''
#!/bin/bash
pacman --noconfirm -S dhcpcd-s6 iwd-s6 openresolv grub efibootmgr connman-s6 connman-gtk vim git curl openssh zsh
s6-rc-bundle-update -c /etc/s6/rc/compiled add default connmand
git clone https://github.com/soerenOsisa/configs /configs
#ZSH
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/powerline/powerline.git
cd powerline
./install.sh
cd ..
rm -rf powerline
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' ~/.zshrc
cat /configs/zshrc >> ~/.zshrc
cp /configs/aur /usr/local/bin/aur
#FONTS
git clone https://github.com/powerline/fonts.git --depth=1
cd fonts
./install.sh
cd ..
rm -rf fonts
chsh -s /usr/bin/zsh
#WINDOW
pacman --noconfirm -S xorg-xinit xorg-server libxft terminus-font nvidia nvidia-utils xorg-xsetroot
nvidia-modprobe
git clone https://github.com/soerenOsisa/dwm /dwm
git clone https://github.com/soerenOsisa/dmenu /dmenu
git clone https://github.com/soerenOsisa/st /st
cd /dwm && make clean install && cd ..
cd /dmenu && make clean install && cd ..
cd /st && make clean install && cd ..
#BOOT
pacman -S grub os-prober efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
cp configs/grub /etc/default/grub
cp configs/boot.png /usr/local/boot.png
#USER
echo -e "{}\\n{}" | passwd
useradd -m -g wheel {}
echo -e "{}\\n{}" | passwd {}
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
#KBD&SYNC
sed -i '/en_US.UTF-8 UTF-8/s/^#//g' /etc/locale.gen
locale-gen
echo 'LANG="en-US.UTF-8"' > /etc/locale.conf
echo "{}" > /etc/hostname
ln -sf /usr/share/zoneinfo/posix/{} /etc/localtime
hwclock --systohc
kbd_mode -u
#PACKAGES
{}
#FINISH
#s6-rc-bundle-update add default iwd dhcpcd
rm -r /configs
exit
'''.format(passwd,passwd,user,passwd,passwd,user,hostname,timez,install)

s6_file = open("6", "w", newline='')
s6_file.write(s6[1:-1])
s6_file.close()
s62_file = open("62", "w", newline='')
s62_file.write(s62[1:-1])
s62_file.close()