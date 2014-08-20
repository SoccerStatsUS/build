echo "oscar" > /etc/hostname
hostname -F /etc/hostname
apt-get update
apt-get upgrade
nano /etc/hosts
dpkg-reconfigure tzdata
adduser chris
usermod -a -G sudo chris
logout

