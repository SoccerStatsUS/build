# for building the website / postgres db

sudo apt-get install python-pip python-dev postgresql-server-dev-all postgresql python3-psycopg2

sudo su - postgres

createuser -s chris
createuser -s soccerstats
logout

# modify  pg_hba.conf to accept local connections on "trust" (this is probably too broad).
# local / local / trust
sudo emacs /etc/postgresql/9.3/main/pg_hba.conf 
sudo service postgresql restart

cd ~/soccer
git clone https://github.com/SoccerstatsUS/s2.git
cd s2

# Edit DEBUG, PROJECT_DIRNAME in custom_settings.py
# Edit SECRET_KEY in secret_settings.py

sudo pip3 install -r requirements3.txt 
./build.sh
