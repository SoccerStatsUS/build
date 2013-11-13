#!/usr/local/bin/env python
# -*- coding: utf-8 -*-


aliases = {}

full_alias = {
    'Rio Branco Cup': 'Copa Rio Branco',

    'Interliga': 'InterLiga',
    'La Ligue': 'Ligue 1',

    'K-League': 'K League',

    'FIFA World Youth Championship': 'FIFA U-20 World Cup',


    'Costa Rican Primera División': 'Primera División de Costa Rica',
    
    'Club World Cup': 'FIFA Club World Cup',

    'Super Lig': 'Süper Lig',
    'Superlig': 'Süper Lig',

    # Once competition mapping is implemented.
    'CONCACAF Champions\' Cup': 'CONCACAF Champions League',
    'Copa Fraternidad Centroamericana': 'Copa Interclubes UNCAF',
    'Torneo Grandes de Centroamerica': 'Copa Interclubes UNCAF',
    'UNCAF Club Championship': 'Copa Interclubes UNCAF',

    'Copa Interamericana': 'Interamerican Cup',
    'Copa Intercontinental': 'Intercontinental Cup',

    'Liga Argentina de Football': 'Argentine Primera División',

    'Brasileirao': 'Campeonato Brasileiro Série A',
    'Brasileirão': 'Campeonato Brasileiro Série A',

    'Chilean Primera Division': 'Chilean Primera División', 
    'Uruguayan Primera Division': 'Uruguayan Primera División',

    'Merconorte Cup': 'Copa Merconorte',

    'Duvalier Cup': 'Coupe Duvalier',
    'Newton Cup': 'Copa Newton',
    'President R.S. Pena Cup': 'Copa Roque Saenz Pena',
    'Juan Pinto Duran Cup': 'Copa Pinto Duran',
    'Argentine Honour Cup': 'Copa Premio Honor Argentino',

    'Uruguayan Honour Cup': 'Copa Premio Honor Uruguayo',

    'CONCACAF Nations Cup': 'CONCACAF Championship',

    'Confederations Cup': 'FIFA Confederations Cup',
    'King Fahd Cup': 'FIFA Confederations Cup',

    'Panamerican Games': 'Pan American Games',
    'Panamerican Games Qualifying': 'Pan American Games Qualifying',
    'South American Championship': 'Copa America',

    'Copa Caribe': 'Caribbean Cup',
    'Copa Caribe Qualifying': 'Caribbean Cup Qualifying',

    'UNCAF Cup': 'Copa Centroamericana',
    'UNCAF Nations Cup': 'Copa Centroamericana',

    #'Copa America': 'Copa América',

    'United Soccer League': 'United Soccer League (1984-1985)',

    'Western Soccer Alliance': 'Western Soccer League',
    'Western Soccer Alliance Playoffs': 'Western Soccer League Playoffs',

    'Southwest Indoor Soccer League': 'United States Interregional Soccer League (indoor)',
    'Southwest Independent Soccer League (indoor)': 'United States Interregional Soccer League (indoor)',
    'Southwest Independent Soccer League': 'United States Interregional Soccer League',

    'US Cup': 'U.S. Cup',
    'USISL Premier League': 'USL Premier Developmental League',

    'USISL Professional League': 'USL Second Division',
    'USL Pro': 'USL Second Division',

    'A-League': 'USL First Division',

    'American Indoor Soccer Association': 'National Professional Soccer League (indoor)',

    'Friendly International': 'International Friendly',

    'Unofficial Friendly': 'Friendly',

    'Recopa CONCACAF': 'CONCACAF Cup Winners Cup',
    'CONCACAF Champions Cup': 'CONCACAF Champions\' Cup',

    'Premier Soccer Alliance': 'World Indoor Soccer League',

    'World Cup': 'FIFA World Cup',

    'FIFA World Cup Qualifying (CONCACAF)': 'FIFA World Cup qualification (CONCACAF)',
    'FIFA World Cup Qualification': 'FIFA World Cup qualification',

    'CONCACAF Men\'s Olympic Qualifying Tournament': 'Olympic Games qualification (CONCACAF)',
    'Olympic Games Qualifying': 'Olympic Games qualification',


    # Just fix...
    'Black Stars': 'Tournoi Black Stars',
    '3 Nations Cup': '3 Nations Tournament',
    'Mexico Cup': 'Mexico City Cup',
    'UNCAF': 'Copa Centroamericana',


}

aliases.update(full_alias)

# Don't want to completely delete these.
partial_alias = {

    'Domestic Tour': 'Friendly',
    'International Tour': 'Friendly',

    'Parmalat Cup': 'Friendly',

    'Desert Diamond Cup': 'Friendly',
    'Chicago Sister Cities International Cup': 'Friendly',

    'U.S. Cup': 'International Friendly',

    'Bicentennial Cup': 'Friendly',
    'Carlsberg Cup': 'Friendly',
    'Carolina Challenge Cup': 'Friendly',
    'Dynamo Charities Cup': 'Friendly',
    'Europac International': 'Friendly',
    'Spring Cup Matches': 'Friendly',
    'Sunshine International': 'Friendly',
    'Toronto International': 'Friendly',
    'Tournament of Champions': 'Friendly',
    'Trans-Atlantic Challenge Cup': 'Friendly',

    'Amistad Cup': 'International Friendly',

    'International Cup': 'International Friendly',
    'Joe Robbie Cup': 'International Friendly',
    'Kirin Cup': 'International Friendly',
    'Los Angeles Soccer Tournament': 'Friendly',
    'Mexico City Tournament': 'International Friendly',
    'Miami Cup': 'International Friendly',
    'North American Nations Cup': 'International Friendly',
    'Presidents Cup': 'International Friendly',
    'Trinidad Tournament': 'International Friendly',
    }
aliases.update(partial_alias)


def get_competition(s):
    if s is None:
        return None
    
    s = s.strip()
    return aliases.get(s, s)
