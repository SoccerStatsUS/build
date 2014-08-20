sudo apt-get install python-pip python-dev postgresql-server-dev-all

git clone https://github.com/Soccerstats/s2.git

sudo su - postgres
createuser -s chris
createuser -s soccerstats

emacs custom_settings.py
emacs secret_settings.py
sudo apt-get install postgresql-server-dev-all python-dev
sudo apt-get install binutils libproj-dev gdal-bin
#sudo apt-get install libxml2-dev
cd s2
pip install -r requirements.txt 
