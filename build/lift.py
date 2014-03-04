from settings import SOURCES

from smid.mongo import generic_load, soccer_db, insert_rows, insert_row, soccer_db

# This is where I convert data like
# Stark (Bethlehem Steel, ASL, 1924-1925) -> Archie Stark

from collections import defaultdict



def lift():
    transform_names_from_rosters()


    print("Transforming names.")
    # Comment this out if worried about over-assigning full names.
    #transform_player_names() 





def transform_names_from_rosters():
    """
    Transform lineup and goal player names based on roster data.
    """

    for source in SOURCES:

        rdb = soccer_db['%s_rosters' % source]

        if rdb.count():

            rg = make_roster_guesser(rdb)

            l = []
            coll = soccer_db["%s_lineups" % source]
            for e in coll.find():
                e['name'] = rg(e['name'], e['team'], e['competition'], e['season'])
                l.append(e)

            coll.drop()
            insert_rows(coll, l)


            g = []
            coll = soccer_db["%s_goals" % source]
            for e in coll.find():

                if 'Own Goal' in e['assists']:
                    #print("skipping og: %s" % e)
                    # Use opponent?
                    continue

                e['goal'] = rg(e['goal'], e['team'], e['competition'], e['season'])
                e['assists'] = [rg(a, e['team'], e['competition'], e['season']) for a in e['assists']]
                g.append(e)

            coll.drop()
            insert_rows(coll, g)




def get_name_from_fragment(fragment, candidates):
    # Need to figure out how to deal with situations like Willie Reid, W. Reid, W.Reid, Reid
    # It's obvious what should happen here. W. Reid gets turned into Willie Reid, then Reid gets turned into Willie Reid
    # But less obvious how to do it.

    if fragment is None:
        return fragment


    cx = [e for e in candidates if e.endswith(fragment) and e != fragment]

    if len(cx) == 1:
        #print("Converting %s to % s" % (fragment, c2[0]))
        return cx[0]

    elif len(cx) > 1:
        #print("Cannot decide between %s for %s" % (str(c2), fragment))
        return fragment

    else:
        # We've failed to find a match. This may be because we have a situation like W. Reid.
        if fragment.count('.') != 1:
            return fragment

        else:
            f1, f2 = fragment.split('.')
            
            # Presumably there should be more than one match. This is why you would include a first initial at all.
            cx = [e for e in candidates if e.endswith(f2) and e != f2]

            # This is the only case where we want produce a match.
            # right?
            matches = []
            for cd in cx:
                if cd.startswith(f1):
                    matches.append(cd)

            if len(matches) == 1:
                return matches[0]

            # This should never happen.
            elif len(matches) > 1:
                print("Ambiguous:", fragment, matches)

    return fragment


def make_roster_guesser(db):
    d = defaultdict(set)
    for e in db.find():
        key = (e['team'], e['competition'], e['season'])
        d[key].add(e['name'])

    def getter(name, team, competition, season):
        key = (team, competition, season)
        candidates = d[key]
        return get_name_from_fragment(name, candidates)

    return getter



def transform_player_names2():
    full_name_guesser = make_player_name_guesser()


    for source in SOURCES:
        l = []
        coll = soccer_db["%s_goals" % source]
        for e in coll.find():
            if e['date']:
                e['goal'] = full_name_guesser(e['goal'], get_team(e['team']))

            l.append(e)
        coll.drop()
        insert_rows(coll, l)


    for source in SOURCES:
        l = []
        coll = soccer_db["%s_lineups" % source]
        for e in coll.find():
            if e['date']:
                e['name'] = full_name_guesser(e['name'], get_team(e['team']))

            l.append(e)
        coll.drop()
        insert_rows(coll, l)




def transform_player_names():
    """
    Generate full names from rosters, player stats.
    """

    full_name_guesser = make_player_name_guesser()

    for source in SOURCES:
        l = []
        coll = soccer_db["%s_goals" % source]
        for e in coll.find():
            if e['date']:
                e['goal'] = full_name_guesser(e['goal'], get_team(e['team']))

            l.append(e)
        coll.drop()
        insert_rows(coll, l)


    for source in SOURCES:
        l = []
        coll = soccer_db["%s_lineups" % source]
        for e in coll.find():
            if e['date']:
                e['name'] = full_name_guesser(e['name'], get_team(e['team']))

            l.append(e)
        coll.drop()
        insert_rows(coll, l)



