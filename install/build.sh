# for building the mongo database

# mongo
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get upgrade

# sudo apt-get install git-core mongodb-org emacs python3-pip  # python3-pip not in ubuntu 12.04
sudo apt-get install git-core mongodb-org emacs python3-setuptools
sudo easy_install3 pip

emacs .bashrc 
# add equivalent to `export PYTHONPATH=$PYTHONPATH:/home/chris/bin:/home/chris/www:/home/chris/repos:/home/chris/soccer`
source .bashrc

mkdir soccer/
cd soccer/

git clone https://github.com/SoccerstatsUS/parse.git
git clone https://github.com/SoccerstatsUS/metadata.git
git clone https://github.com/SoccerstatsUS/nwsl-data.git
git clone https://github.com/SoccerstatsUS/build.git


cd build/
sudo pip3 install -r requirements3.txt 

python3 run/main.py 
