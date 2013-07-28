import datetime
import re

from soccerdata.data.alias import get_team, get_name

# Need to add in new positions.
POSITIONS_PATH = '/home/chris/www/soccerdata/data/transactions/positions'

class PositionParser(object):
    """
    Parse position text file.
    e.g. Bruce Arena, Head Coach, DC United, 1996, 1998
    """
    # Empty person, position, or team fields will be repeated from the previous line.

    def __init__(self):
        self.person = None
        self.position = None
        self.team = None

    def process_date_string(self, s, end=False):
        # A date string is either a full date or just a year, depending on data quality.
        # If the date is just a year, we call it the first day of the year if it is the start of a job,
        # and the last day of the year if it is the end of a job.

        # This is problematic with seasons like 1922-1923 in which multiple years are played.
        s = s.strip()
        if not s:
            return None

        m = re.match("(\d+)/(\d+)/(\d+)", s) # something like 12/31/1989
        if m:
            month, day, year = [int(e) for e in m.groups()]
        else:
            if end == False:
                month, day, year = 1, 1, int(s) 

            else:
                month, day, year = 12, 31, int(s)

        d = datetime.datetime(year, month, day)

        return d


    def process_line(self, line):
        # Does date handling and fills in empty fields if necessary.
        fields = line.split(",")

        person, position, team = [e.strip() for e in fields[:3]]

        start = end = None
        if len(fields) > 3:
            start = self.process_date_string(fields[3])
        if len(fields) > 4:
            end = self.process_date_string(fields[4], end=True)

        # Set state variables if necessary.
        if person:
            self.person = person
        if position:
            self.position = position
        if team:
            self.team = get_team(team)

        return {
            'person': get_name(self.person),
            'name': self.position,
            'team': get_team(self.team),
            'start': start,
            'end': end,
            }


def process_position_file(fn):
    """Process a file."""
    p = PositionParser()
    return [p.process_line(e) for e in open(fn)]

process_positions = lambda: process_position_file(POSITIONS_PATH)

if __name__ == "__main__":
    print(process_positions())



            
