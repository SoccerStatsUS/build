import os
import sys

from smid.settings import ROOT_DIR

# Figure out way to dynamically get virtualenv
sys.path.append(os.path.join(ROOT_DIR, '.virtualenvs/soccerdata/lib/python2.6/site-packages'))
sys.path.append(os.path.join('/home/chris', 'www')

logfile = os.path.join('www/smid/logs/gunicorn.log')

bind = "127.0.0.1:29111"
workers = 3
