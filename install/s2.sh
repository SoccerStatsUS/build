# for building the website / postgres db

sudo apt-get install python-pip python-dev postgresql-server-dev-all 
sudo apt-get install postgresql
sudo apt-get install python3-psycopg2

# Geodjango
# sudo apt-get install binutils libproj-dev gdal-bin libxml2-dev

sudo su - postgres

createuser -s chris
createuser -s soccerstats
logout

# modify  pg_hba.conf to accept local connections on "trust" (this is probably too broad).
# could be /9.1/
sudo emacs /etc/postgresql/9.3/main/pg_hba.conf 
sudo service postgresql restart

cd ~/soccer
git clone https://github.com/Soccerstats/s2.git
cd s2

# Add DEBUG, PROJECT_DIRNAME to custom_settings
emacs custom_settings.py

# Add SECRET_KEY to secret_settings.
emacs secret_settings.py

sudo pip install -r requirements.txt 
./build.sh
