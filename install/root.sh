# for performing first, as root.

echo "oscar" > /etc/hostname
hostname -F /etc/hostname
nano /etc/hosts

dpkg-reconfigure tzdata
adduser chris
usermod -a -G sudo chris

logout

