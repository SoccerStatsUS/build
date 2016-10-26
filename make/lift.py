from settings import SOURCES

from build.mongo import generic_load, soccer_db, insert_rows, insert_row, soccer_db

# This is where I convert data like
# Stark (Bethlehem Steel, ASL, 1924-1925) -> Archie Stark

from collections import defaultdict



def lift():
    print("Lifting names")
    transform_names_from_rosters()


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


            """
            f = []
            coll = soccer_db["%s_fouls" % source]
            for e in coll.find():

                e['goal'] = rg(e['goal'], e['team'], e['competition'], e['season'])
                e['assists'] = [rg(a, e['team'], e['competition'], e['season']) for a in e['assists']]
                g.append(e)
            """



            coll.drop()
            insert_rows(coll, g)





def get_name_from_fragment(fragment, candidates):
    # Need to figure out how to deal with situations like Willie Reid, W. Reid, W.Reid, Reid
    # It's obvious what should happen here. W. Reid gets turned into Willie Reid, then Reid gets turned into Willie Reid
    # But less obvious how to do it.

    from helpers import string_to_ascii


    if fragment is None:
        return fragment

    #if fragment == 'A. Munoz':
    #    import pdb; pdb.set_trace()

    ascii_fragment = string_to_ascii(fragment)

    cx = [full for (ascii, full) in candidates if ascii.endswith(ascii_fragment) and ascii != ascii_fragment]


    if len(cx) == 1:
        #print("Converting %s to % s" % (fragment, c2[0]))
        return cx[0]

    elif len(cx) > 1:
        #print("Cannot decide between %s for %s" % (str(c2), fragment))
        return fragment

    else:

        # We've failed to find a match. This may be because we have a situation like W. Reid.
        # This doesn't seem to do anything.
        if fragment.count('.') == 1:
            f1, f2 = ascii_fragment.split('.')
            
            # Presumably there should be more than one match. This is why you would include a first initial at all.
            cx = [(ascii, full) for (ascii, full) in candidates if ascii.endswith(f2) and ascii != f2]

            # This is the only case where we want produce a match.
            # right?
            matches = []
            for (ascii, full) in cx:
                if ascii.startswith(f1):
                    matches.append(full)

            if len(matches) == 1:
                return matches[0]

            # This should never happen.
            elif len(matches) > 1:
                print("Ambiguous:", fragment, matches)

        else:
            # Handle situations like Sabah -> Miguel Sabah Gerardo
            # name embedded inside longer name. 
            padded_fragment = ' %s ' % ascii_fragment
            matches = [(ascii, full) for (ascii, full) in candidates if padded_fragment in ascii]

            if len(matches) == 1:
                return matches[0][1]


    return fragment


def make_roster_guesser(db):
    d = defaultdict(set)
    for e in db.find():
        key = (e['team'], e['competition'], e['season'])
        #d[key].add(e['name'])
        d[key].add((e['ascii_name'], e['name']))

    def getter(name, team, competition, season):
        key = (team, competition, season)
        candidates = d[key]
        return get_name_from_fragment(name, candidates)
    
    #getter.d = d # for debugging

    return getter
