import os
import sys

from smid.settings import ROOT_DIR

# Rethink this approach...probably split out soccerdata website from build process.
# Figure out way to dynamically get virtualenv
# This will not work with other computers.

sys.path.append(os.path.join(ROOT_DIR, '.virtualenvs/soccerdata/lib/python2.6/site-packages'))
sys.path.append(ROOT_DIR)


logfile = os.path.join('www/smid/logs/gunicorn.log')

bind = "127.0.0.1:29111"
workers = 3
