#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

from soccerdata.build.normalize import make_stadium_getter

sg = make_stadium_getter()

def test_stadium_alias():
    assert_equal(sg('DSG Park'), ("Dick's Sporting Goods Park", 'Commerce City, CO'))

def test_stadium_normal():
    assert_equal(sg("Dick's Sporting Goods Park"), ("Dick's Sporting Goods Park", 'Commerce City, CO'))

def test_stadium_unicode():
    assert_equal(sg('Estadio Cuscatlán'), (u'Estadio Cuscatlán', 'San Salvador, El Salvador'))
