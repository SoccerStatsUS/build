"""
Goal of this package is to completely build all soccer statistics
for the site.

That is to say, import all of them into mongo, and possibly check for consistency.

After that, create canonical lists that can be used for viewing or 
imported into socceroutsider.com for better relationships, etc.
"""

from load import load
from generate import generate
from check import check
from merge import merge
from normalize import normalize
from denormalize import denormalize
from transform import transform
from lift import lift

# Load all possible games into various collections.
# Try to merge all of those into a single games database.

# Generate standings from games.
# Check generated standings against loaded standings.
# Load wikipedia standings for competitions that don't have them.

# Load goals
# Check goals against games.

import os
import sys


def timer(method):

    import time

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed



def build():
    """

    Convert unstructured data (text and web) into structure data in a mongo database.
    Load data, normalize it, 
    """

    try:
        unicode
        print("Please use Python3")
        return
    except:
        pass


    for func in [
        load, 
        normalize, 
        lift,
        transform, 
        merge, 
        generate, 
        denormalize, 
        #check
        ]:
        print(func.__name__)
        timer(func)()
    
    return

    # Do you want to generate before so that you can use / merge those items normally?
    # Or do you want to generate afterwards so that you can filter things easier?
    #timer(load())

    # This is where player, team, competition, and place names are normalized.
    # Best to do this as early as possible.
    #timer(normalize())

    # e.g. United States -> United States U-17
    # Transform names like Carnihan -> Bill Carnihan if possible.
    # Split names like Arsenal (in Argentina D1) -> Arsenal de Sarandi.
    #timer(transform())

    # Nothing happens here anymore.
    # Generating for individual collections
    #print("generate")
    #timer(generate())

    # Merge everything together.
    #timer(merge())

    # Generating game stats, competition standings and stats.
    #timer(generate())

    # Convert names like FC Dallas -> Dallas Burn, e.g. 
    #timer(denormalize())
    
    # Check data sanity? not heavily used.
    #timer(check())


if __name__ == "__main__":
    build()


