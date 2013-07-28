import datetime
import os

from soccerdata.data.transactions.coach import transactions

def process_manager_list():
    """
    Converts 
      ("Bob Gansler", "KC", (2009,1,1), None), 
      ("Brian Bliss", "KC", (2010,1,1), (2011,1,1)),
    to {
        'name': 'Bob Gansler', 
        'team': 'Sporting Kansas City', 
        'start': datetime.date(2009,1,1),
        'end': datetime.date(2010,1,1)
        }
    """
    l = []
    for name, team, start, end in transactions:
        if start:
            start = datetime.date(*start)
        if end:
            end = datetime.date(*end)


        if start is None:
            previous =  l[-1]
            start = previous['end']

        if l:
            previous =  l[-1]
            if previous['end'] is None:
                if team == previous['team']:
                    previous['end'] = start

        l.append({
                'name': name,
                'team': team,
                'start': start,
                'end': end,
                })
    return l
            

if __name__ == "__main__":
    print(process_manager_list())
