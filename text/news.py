import datetime
import os
import re

# FIXME
NEWS_FILE = "/home/chris/www/soccerdata/data/news"

def load():
    l = []
    for line in open(NEWS_FILE):
        if line.strip():
            line = line.strip()
            name, url = line.split(',')
            l.append({
                    'name': name,
                    'url': url,
                    })
    return l
            

if __name__ == "__main__":
    print(load())
