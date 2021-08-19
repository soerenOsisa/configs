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

s6base = '''
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
basestrap /mnt base base-devel s6-base elogind elogind-s6 linux-zen linux-firmware dhcpcd-s6 iwd-s6 openresolv grub os-prober efibootmgr connman-s6 connman-gtk vim git openssh htop
fstabgen -U /mnt >> /mnt/etc/fstab
modprobe efivarfs
cat configs/s6configs | artix-chroot /mnt /bin/bash
umount -R /mnt
reboot
'''.format(drive,boot)
s6configs='''
#!/bin/bash
s6-rc-bundle-update -c /etc/s6/rc/compiled add default connmand
git clone https://github.com/soerenOsisa/configs /configs
cp /configs/.bashrc ~/.bashrc
cp /configs/aur /usr/local/bin/aur
echo "[[ -f ~/.profile ]] && . ~/.profile" > ~/.bash_profile
useradd paur
echo "paur ALL=(ALL) NOPASSWD: /usr/bin/makepkg" >> /etc/sudoers
sh /configs/s6desktop
'''
s6desktop='''
#!/bin/bash
pacman --noconfirm -S xorg nvidia nvidia-utils
#pacman --noconfirm -S xorg xf86-video-amdgpu amdgpu-pro-libgl
#pacman --noconfirm -S xorg xf86-video-intel mesa
#pacman --noconfirm -S xorg xf86-video-fbdev xf86-video-vesa
nvidia-modprobe
/usr/local/bin/aur librewolf
/usr/local/bin/aur mailspring
git clone https://github.com/Axarva/dotfiles-2.0
cd dotfiles-2.0
chmod +x install-on-arch.sh
echo -e "3\\nyes\\ny\\ny\\ny\\n2\\ny\\nN\\ny\\n2\\ny\\n" | ./install-on-arch.sh
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' ~/.zshrc
echo 'export PATH="$PATH:/home/{}/bin"' >> ~/.zshrc
echo 'export PATH="$PATH:~/bin"' >> ~/.zshrc
xmonad --recompile
#sed -i "s/loginctl/s6-rc/g" ~/bin/powermenu.sh
cat /configs/.bashrc >> ~/.zprofile
echo "startx" >> ~/.zprofile
echo "exec xmonad" >> ~/.xinitrc
sed -i "s/9/12/g" ~/.config/alacritty.yml
sh /configs/s6boot
'''.format(user)
s6boot='''
#!/bin/bash
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
cp /configs/grub /etc/default/grub
cp /configs/boot.png /usr/local/boot.png
update-grub
sh /configs/s6user
'''
s6user='''
#!/bin/bash
echo -e "{}\\n{}" | passwd
useradd -m -g wheel {}
echo -e "{}\\n{}" | passwd {}
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
sh /configs/s6locale
'''.format(passwd,passwd,user,passwd,passwd,user)
s6locale='''
#!/bin/bash
sed -i '/en_US.UTF-8 UTF-8/s/^#//g' /etc/locale.gen
locale-gen
echo 'LANG="en-US.UTF-8"' > /etc/locale.conf
echo "{}" > /etc/hostname
ln -sf /usr/share/zoneinfo/posix/{} /etc/localtime
hwclock --systohc
kbd_mode -u
sh /configs/s6finish
'''.format(hostname,timez)
s6finish='''
#!/bin/bash
{}
#FINISH
#s6-rc-bundle-update add default iwd dhcpcd
rm -r /configs
exit
'''.format(install)

def s6script(name,var):
	s6f = open(name, "w", newline='')
	s6f.write(var[1:-1])
	s6f.close()

s6script('s6base',s6base)
s6script('s6configs',s6configs)
s6script('s6desktop',s6desktop)
s6script('s6boot',s6boot)
s6script('s6locale',s6locale)
s6script('s6user',s6user)