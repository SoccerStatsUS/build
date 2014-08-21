# for launching the site

./update.sh

# sudo apt-get install nginx

# move soccerstats.us file from files/nginx to /etc/nginx/sites-available
# symlink to sites-enabled

# exec sudo -u chris $VENV/bin/gunicorn_django --preload -w 1 --log-level debug --log-file $SITE/run/dev.log -p $SITE/run/dev.pid -b 127.0.0.1:29002 $SITE/settings.py

export SITE="/home/chris/soccer/s2"
sudo gunicorn_django --preload -w 1 --log-level debug --log-file $SITE/run/dev.log -p $SITE/run/dev.pid -b 127.0.0.1:29002 $SITE/settings.py

python3 manage.py runserver
