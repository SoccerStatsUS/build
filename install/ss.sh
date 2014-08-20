cd ~
sudo apt-get update
sudo apt-get install git-core python3-pip mongodb-org emacs
emacs .bashrc 
# add equivalent to export PYTHONPATH=$PYTHONPATH:/home/chris/bin:/home/chris/www:/home/chris/repos:/home/chris/soccer
mkdir soccer/
cd soccer/
git clone https://github.com/Soccerstats/build.git
git clone https://github.com/Soccerstats/parse.git
git clone https://github.com/Soccerstats/soccerdata.git
git clone https://github.com/Soccerstats/conmebol-data.git

cd build/
sudo pip3 install -r requirements3.txt 

