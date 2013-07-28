
# FIXME
SALARIES_PATH = "/home/chris/www/soccerdata/data/money/salaries/mls.csv"
MLS_SALARIES_PATH = "/home/chris/www/soccerdata/data/money/salaries/%s"



def load_salaries():
    s1 = load_old_salaries()
    for e in range(2011, 2014):
        s1 += load_new_salaries(MLS_SALARIES_PATH % e, e)
    return [e for e in s1 if e]


def load_old_salaries():
    """
    Load MLS salaries
    """

    def process_line(line):
        # Remove trailing newline.
        if line.endswith("\n"):
            line = line[:-1]


        try:
            year, team, last_name, first_name, _, base, extra = line.split('\t')
        except:
            import pdb; pdb.set_trace()

        name = "%s %s" % (first_name.strip(), last_name.strip())

        if 'Twellman' in name:
            pass #import pdb; pdb.set_trace()

        return {
            'name': name,
            'year': year,
            'team': team,
            'base': base,
            'extra': extra,
            }

    f = open(SALARIES_PATH)
    return [process_line(line) for line in f]


def load_new_salaries(fn, year):
    """
    Load MLS salaries
    """

    def process_line(line):
        # Remove trailing newline.

        if not line.strip():
            return


        if line.endswith("\n"):
            line = line[:-1]

        try:
            team, n, base, extra = line.split(';')
        except:
            import pdb; pdb.set_trace()

        if ',' in n:
            last_name, first_name = [e.strip() for e in n.split(',')]
            name = "%s %s" % (first_name, last_name)
        else:
            print(n)
            name = n

        return {
            'year': year,
            'name': name,
            'team': team,
            'base': base,
            'extra': extra,
            }

    f = open(fn)
    return [process_line(line) for line in f]
