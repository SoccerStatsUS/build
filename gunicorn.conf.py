import os
import sys

# Figure out way to dynamically get virtualenv
sys.path.append("/home/chris/.virtualenvs/soccerdata/lib/python2.6/site-packages")
sys.path.append("/home/chris/www")


bind = "127.0.0.1:29111"
logfile = "/home/chris/www/soccerdata/logs/gunicorn.log"
workers = 3
