echo "oscar" > /etc/hostname
hostname -F /etc/hostname
nano /etc/hosts

apt-get update
apt-get upgrade

dpkg-reconfigure tzdata
adduser chris
usermod -a -G sudo chris

logout

