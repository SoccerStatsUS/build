#!/usr/local/bin/env python
# -*- coding: utf-8 -*-


# Load stats from excel files.

import os


# FIXME
DIR = '/home/chris/www/soccerdata/data/stats'

if not os.path.exists(DIR):
    DIR = "/Users/chrisedgemon/www/soccerdata/data/stats"


def process_mls_2012_stats():
    return process_stats("d1/2012", "Major League Soccer", source='MLSSoccer.com')


def process_mls_coach_stats():
    return process_stats("d1/mls.coaches", "Major League Soccer", source='MLSSoccer.com')

def process_nasl_stats():
    return process_stats("d1/nasl", format_name=False, source='nasljerseys.com')

def process_misl_stats():
    return process_stats("indoor/misl", format_name=False, source='nasljerseys.com')



def process_usl1_stats():
    l = []
    l.extend(process_stats("d2/19972005", "USL First Division"))

    for e in '06', '07', '08', '09', '11', '12':
        l.extend(process_stats("d2/20%s" % e, "USL First Division"))

    return l

def process_usl2_stats():
    l = []
    l.extend(process_stats("d3/psl", "USL Second Division"))
    l.extend(process_stats("d3/20052009", "USL Second Division"))
    for e in range(2010, 2013):
        l.extend(process_stats("d3/%s" % e, "USL Pro"))

    return l

def process_pdl_stats():
    l = []
    for e in range(2003, 2013):
        l.extend(process_stats("d4/%s" % e, "USL Premier Developmental League"))
    return l

    
def process_name(s):

    if ',' not in s:
        return s

    mapping = {
        'Da Silva-Sarafim, Jr, Edivaldo': 'Da Silva-Sarafim Jr, Edivaldo',
        'Novas, Lomonaca, Ignacio': 'Novas, Ignacio',
        'Kato, Hajime,': 'Kato, Hajime',
        'Kolba, JR., Thoms': 'Kolba Jr., Thomas',
        'Fragoso-Gonzalez, Jr, Pedro': 'Fragoso-Gonzalez Jr, Pedro',
        }

    if s in mapping:
            s = mapping[s]

    try:
        last, first = [e.strip() for e in s.split(',')] # Assume no 2-comma names.    
    except:
        import pdb; pdb.set_trace()
    name = first + ' ' + last
    if '*' in name:
        import pdb; pdb.set_trace()
    name = name.replace("*", "")
    return name.strip()



def process_stats(fn, competition=None, format_name=True, source=None):

    def preprocess_line(line):
        # Should probably just process these text files.
        line = line.replace('\xa0', '')
        line = line.replace('\xc2', '')
        
        # Remove *'s from nasl stats.
        line = line.replace("*", "")
        line = line.strip()
        return line


    def stat_fixes(d):
        # Incorrect line in naslmisl.csv
        if d.get('name') == 'Santiago Formoso':
            if d.get('games_played') == 'D':
                d.update({'games_played': '5', 'goals': '0'})
        return d
                         
    def process_line(line):
        line = preprocess_line(line)

        if not line:
            return {}

        fields = line.split('\t')
        d = dict(zip(header, fields))
        d = stat_fixes(d)
        

        if 'name' not in d:
            return {}

        if not d['name']:
            return {}


        if format_name:
            d['name'] = process_name(d['name'])

        if competition is not None:
            d['competition'] = competition

        if source is not None:
            d['source'] = source

        if 'year' in d:
            d['season'] = d.pop('year')
        else:
            try:
                d['season'] = d['season']
            except:
                import pdb; pdb.set_trace()



        if 'games' in d:
            d['games_played'] = d.pop('games')
            
        for k in 'games_played', 'games_started', 'minutes', 'goals', 'assists', 'shots', 'shots_on_goal', \
                'blocks', 'fouls_committed', 'fouls_suffered', 'offsides', 'pk_goals', 'pk_attempts', 'pks_drawn', \
                'pks_committed':
            if k in d:
                v = d[k]
                v = v.strip()

                if v in ('', '-'):
                    v = 0
                elif v == '?':
                    v = None
                else:
                    try:
                        d[k] = int(v)
                    except ValueError:
                        print(v)

            if 'position' in d:
                d.pop('position')
            if 'points' in d:
                d.pop('points')

        d['position'] = ''
        return d

    path = os.path.join(DIR, fn)
    lines = open(path).read().strip().split('\n')
    header = lines[0].split('\t')
    l = [process_line(line) for line in lines[1:]]
    return [e for e in l if e]


