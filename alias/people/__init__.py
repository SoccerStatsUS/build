#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

#from django.template.defaultfilters import slugify

from smid.alias.people.partial import partial
from smid.alias.people.last import last_names
from smid.alias.people.nonpeople import nonpeople
from smid.alias.people.usmnt import usmnt
from smid.alias.people.basic import basic

def get_name(name):
    # Add last name normalize option?
    # Need to fill in rosters before normalizing?

    name = name.strip()

    if name in names:
        nname = get_name(names[name])
        if nname in names:
            print(nname)
        return nname
    return name


# Handle name loops before processing everything.
def check_for_name_loops():
    errors = False
    for e in names.keys():
        try:
            get_name(e)
        except:
            import pdb; pdb.set_trace()
            print(e)
            errors = True

    if errors:
        print(errors)
        raise Exception



names = {}





names.update(basic)
names.update(nonpeople)
names.update(partial)
names.update(last_names)
names.update(usmnt)


check_for_name_loops()
