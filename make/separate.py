#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

from metadata.alias import get_team, get_competition




# Use a partial? memoize?
def from_competition(competition):

    c2 = get_competition(competition)
    return lambda d: get_competition(d['competition']) == c2


def from_seasons(competition, seasons):
    return lambda d: from_competition(competition)(d) and d['season'] in seasons


sep_names = {


    'Alex': [
        ('Alex Monteiro de Lima', {'team': 'Chicago Fire' }),
        ('Alex Monteiro de Lima', {'team': 'Chicago Fire Reserves' }),

        ('Alex Raphael Meschini', {'team': 'Corinthians', 'season': '2012'}),
        ('Alex Raphael Meschini', {'team': 'Corinthians', 'season': '2011'}),
        ('Alex Raphael Meschini', {'team': 'Internacional', 'season': '2006'}),
        ('Alex Raphael Meschini', {'team': 'Internacional', 'season': '2007'}),
        ('Alex Raphael Meschini', {'team': 'Internacional', 'season': '2008'}),

        ('Alex Terra', {'team': 'Melbourne Heart'}),
        ('Alex Terra', {'team': 'Fluminense', 'season': '2005'}),
        ('Alex Terra', {'team': 'Fluminense', 'season': '2004'}),

        ('Alex Rodrigo Dias da Costa', {'team': 'Chelsea'}),
        ('Alex Rodrigo Dias da Costa', {'team': 'PSV Eindhoven'}),
        ('Alex Rodrigo Dias da Costa', {'team': 'Santos FC'}),

        ],


    'Cassio': [
        ('Cássio Oliveira', {'team': 'New England Revolution' }),
        ('Cássio Oliveira', {'team': 'New England Revolution Reserves' }),
        ('Cássio Oliveira', {'team': 'Adelaide United' }),

        ('Cássio Ramos', {'team': 'Corinthians'}),

        ('Cássio Alessandro de Souza', {'team': 'Fluminense'}),
        ('Cássio Alessandro de Souza', {'team': 'Avai FC'}),
        ],




    'Chris Brown': [
        ('Chris Brown (1971)', {'team': 'FC Dallas' }),
        ('Chris Brown (1971)', {'team': 'Richmond Kickers' }),
        ('Chris Brown (1971)', {'team': 'Tampa Bay Terror' }),
        ('Chris Brown (1971)', {'team': 'New Orleans Riverboat Gamblers' }),
        ('Chris Brown (1971)', {'team': 'Maryland Mania' }),
        ],


    'Dejair': [
        ('Dejair Jorge Ferreira', {'team': 'Chivas USA' }),
        ],

    'Denilson': [
        ('Denílson de Oliveira Araújo', {'team': 'FC Dallas' }),
        ('Denílson de Oliveira Araújo', {'team': 'Palmeiras' }),
        ('Denílson de Oliveira Araújo', {'team': 'Real Betis' }),
        ('Denílson de Oliveira Araújo', {'team': 'Flamengo' }),

        ('Denílson Pereira Neves', {'team': 'Arsenal' }),

        ('Denílson Martins Nascimento', {'team': 'Pohang Steelers'}),
        ('Denílson Martins Nascimento', {'team': 'Mogi Mirim'}),

        ],

    'Eduardo': [
        ('Eduardo Adelino da Silva', {'team': 'San Jose Earthquakes' }),
        ],

    'Erick': [
        ('Erick Neres da Cruz', {'team': 'FC Dallas', }),
        ('Erick Neres da Cruz', {'team': 'FC Dallas Reserves', }),
        ],


    'Felipe': [
        ('Felipe Jorge Loureiro', {'team': 'Vasco da Gama', }),
        ],

    'Fred': [
        ('Frederico Chaves Guedes', {'team': 'Fluminense'}),
        ('Frederico Chaves Guedes', {'team': 'Cruzeiro'}),
        ('Frederico Chaves Guedes', {'team': 'Atletico Mineiro'}),

        ('Fred Carreiro', {'team': 'DC United' }),
        ('Fred Carreiro', {'team': 'Philadelphia Union' }),

        ('Frederico Rodrigues de Paula Santos', {'team': 'Internacional'}),
        ],


    'Indio': [
        ('Marcos Antônio de Lima', {'team': 'Internacional' }),
        ('Marcos Antônio de Lima', {'team': 'EC Juventude', 'season': '2004', }),
        ('Marcos Antônio de Lima', {'team': 'EC Juventude', 'season': '2003', }),
        ('Marcos Antônio de Lima', {'team': 'EC Juventude', 'season': '2002', }),

        ],

    'Jenison': [
        ('Jenison Brito', {'team': 'Fort Lauderdale Striekrs', }),
        ],

    #'Geovanni': [
    #    ('Geovanni Deiberson Maurício', {'team': 'San Jose Earthquakes'}),
    #    ('Geovanni Deiberson Maurício', {'team': 'Hull City'}),
    ##    ('Geovanni Deiberson Maurício', {'team': 'SL Benfica'}),
    #    ('Geovanni Deiberson Maurício', {'team': 'Cruzeiro'}),
    #    ],


    'Gilmar': [
        ('Gilmar Antônio Batista', {'team': 'Tampa Bay Mutiny' }),
        ('Gilmar Antônio Batista', {'team': 'Metrostars' }),

        ('Gylmar dos Santos Neves', {'team': 'Santos FC'}),
        #('Gylmar dos Santos Neves', {'team': 'Corinthians'}),

        ('Gilmar Lobato da Rocha', {'team': 'Varzim' }),
        ('Gilmar Lobato da Rocha', {'team': 'Deportes Naval' }),
        ],

    'Jackson': [
        ('Jackson Henrique Gonçalves Pereira', {'team': 'FC Dallas', }),
        ('Jackson Henrique Gonçalves Pereira', {'team': 'Toronto FC', }),
        ],



    'Jenison': [
        ('Jenison Brito', {'team': 'Fort Lauderdale Strikers', }),
        ],

    'Jorge Flores': [
        ('Jorge Villafaña', {'team': 'Chivas USA' }),
        ('Jorge Villafaña', {'team': 'Chivas USA Reserves' }),
        ],

    'Juninho': [
        ('Juninho Paulista', {'team': 'Middlesbrough' }),
        ('Juninho Paulista', {'team': 'Sao Paulo FC', 'season': 1993 }),
        ('Juninho Paulista', {'team': 'Sao Paulo FC', 'season': 1994 }),
        ('Juninho Paulista', {'team': 'Sao Paulo FC', 'season': 1995 }),

        ('Juninho Pernambucano', {'team': 'New York Red Bulls' }),
        ('Juninho Pernambucano', {'team': 'Vasco da Gama' }), #

        ('Vitor Gomes Pereira Júnior', {'team': 'LA Galaxy' }),

        ('Carlos Alberto Carvalho dos Anjos Junior', {'team': 'Kashima Antlers' }),
        ('Carlos Alberto Carvalho dos Anjos Junior', {'team': 'Palmeiras', 'season': '2002' }),
        ('Carlos Alberto Carvalho dos Anjos Junior', {'team': 'Palmeiras', 'season': '2000' }),
        ],

    'Kleber': [
        ('Kléber de Carvalho Corrêa', {'team': 'Corinthians',}),
        ('Kléber de Carvalho Corrêa', {'team': 'Internacional'}),

        ('Kléber Pereira', {'team': 'Atlético Paranaense'}),
        ('Kléber Pereira', {'team': 'Santos FC'}),
        ('Kléber Pereira', {'team': 'Necaxa'}),
        ('Kléber Pereira', {'team': 'Veracruz'}),
        ('Kléber Pereira', {'team': 'Club America'}),
        ('Kléber Pereira', {'team': 'UANL'}),

        ('Kléber de Souza Freitas', {'team': 'Gremio'}),
        ],


    # Also marquinhos...
    'Marquinho': [
        ('Marco Antônio de Mattos Filho', {'team': 'Fluminense'}),
        ('Marco Antônio de Mattos Filho', {'team': 'Figueirense'}),

        ('Marco Antônio dos Santos', {'team': 'Colorado Rapids' }),
        ('Marco Antônio dos Santos', {'team': 'Sport Boys' }),
        ('Marco Antônio dos Santos', {'team': 'Sporting Cristal' }),
        
        ],


    'Luizao': [
        ('Luiz Bombonato Goulart', {'team': 'Hertha BSC',}),
        ('Luiz Bombonato Goulart', {'team': 'Gremio', 'season': '2002'}),
        ('Luiz Bombonato Goulart', {'team': 'Corinthians'}),
        ('Luiz Bombonato Goulart', {'team': 'Vasco da Gama'}),
        ('Luiz Bombonato Goulart', {'team': 'Club Guarani'}),
        ],



    'Maykon': [
        ('Maykon Daniel Elias Araújo', {'team': 'Ottawa Fury' }),
        ],

    'Michel': [
        ('Michel Garbini Pereira', {'team': 'FC Dallas', }),
        ('Michel Garbini Pereira', {'team': 'Atletico Paranaense', 'season': '2007'}),
        ('Michel Garbini Pereira', {'team': 'Atletico Paranaense', 'season': '2006'}),
        ('Michel Garbini Pereira', {'team': 'Atletico Mineiro', 'season': '2003'}),
        ('Michel Garbini Pereira', {'team': 'Atletico Mineiro', 'season': '2002'}),

        ],

    'Naldo': [
        ('Ednaldo da Conceição', {'team': 'LA Galaxy'}),
        ('Ednaldo da Conceição', {'team': 'Los Angeles Galaxy Reserves'}),
        ('Ednaldo da Conceição', {'team': 'California Cougars'}),

        ('Ronaldo Aparecido Rodrigues', {'team': 'Werder Bremen'}),
        ('Ronaldo Aparecido Rodrigues', {'team': 'EC Juventude'}),
        
        ],

    'Nene': [
        ('Fábio Camilo de Brito', {'team': 'Urawa Red Diamonds' }),

        ('Anderson Luiz de Carvalho', {'team': 'Monaco' }),
        ('Anderson Luiz de Carvalho', {'team': 'Celta Vigo' }),
        ('Anderson Luiz de Carvalho', {'team': 'Deportivo Alaves' }),
        ('Anderson Luiz de Carvalho', {'team': 'Mallorca' }),
        ('Anderson Luiz de Carvalho', {'team': 'Santos FC', 'season': '2002', }),
        ('Anderson Luiz de Carvalho', {'team': 'Palmeiras','season': '2001', }),

        ('Ânderson Miguel da Silva', {'team': 'Cagliari'}),
        ('Ânderson Miguel da Silva', {'team': 'CD Nacional'}),
        ('Ânderson Miguel da Silva', {'team': 'Cruzeiro'}),
        ('Ânderson Miguel da Silva', {'team': 'Santa Cruz'}),
        
        ],

    'Oliver': [
        ('Oliver Minatel', {'team': 'Ottawa Fury' }),
        ],


    'Oscar': [
        ('José Oscar Bernardi', {'team': 'Ponte Preta', 'season': '1977' }),
        ('José Oscar Bernardi', {'team': 'New York Cosmos' }),
        ('José Oscar Bernardi', {'team': 'Sao Paulo FC', 'season': '1984' }),
        ('José Oscar Bernardi', {'team': 'Sao Paulo FC', 'season': '1985' }),
        ('José Oscar Bernardi', {'team': 'Sao Paulo FC', 'season': '1986' }),

        ('Óscar García Junyent', {'team': 'FC Barcelona'}),
        ('Óscar García Junyent', {'team': 'Valencia'}),
        ('Óscar García Junyent', {'team': 'RCD Espanyol'}),

        ('Óscar González Marcos', {'team': 'Real Valladolid'}),
        ('Óscar González Marcos', {'team': 'Real Zaragoza'}),

        ('Oscar dos Santos Emboaba Júnior', {'team': 'Internacional'}),


        

        ],


    'Pablo Hernandez': [
        ('Pedro Pablo Hernández', {'team': 'DC United', }),
        ],

    'Pablo Campos': [
        ('Pablo Campos Zamorano', {'team': 'Cruz Azul'}),
        ],

    'Ramon': [
        ('Ramon Menezes Hubner', {'team': 'Cruzeiro', 'season': '1988'}),
        ('Ramon Menezes Hubner', {'team': 'Cruzeiro', 'season': '1989'}),
        ('Ramon Menezes Hubner', {'team': 'Cruzeiro', 'season': '1990'}),
        ('Ramon Menezes Hubner', {'team': 'Cruzeiro', 'season': '1991'}),
        ('Ramon Menezes Hubner', {'team': 'EC Vitoria', 'season': '1994'}),
        ('Ramon Menezes Hubner', {'team': 'Vasco da Gama', 'season': '1996'}),
        ('Ramon Menezes Hubner', {'team': 'Vasco da Gama', 'season': '1997'}),
        ('Ramon Menezes Hubner', {'team': 'Vasco da Gama', 'season': '1998'}),
        ('Ramon Menezes Hubner', {'team': 'Vasco da Gama', 'season': '1999'}),
        ('Ramon Menezes Hubner', {'team': 'Vasco da Gama', 'season': '2000'}),
        ('Ramon Menezes Hubner', {'team': 'Atletico Mineiro', 'season': '2001'}),
        ('Ramon Menezes Hubner', {'team': 'Atletico Paranaense', 'season': '2007'}),
        ('Ramon Menezes Hubner', {'team': 'EC Vitoria', 'season': '2010'}),

        ],

    'Reinaldo': [
        ('Reinaldo de Souza', {'team': 'Botafogo'}),

        ('José Reinaldo de Lima', {'team': 'Atletico Mineiro'}), # there is a second reinaldo for mineiro

        ],


    'Ricardinho': [
        ('Ricardo Alves Pereira', {'team': 'FC Dallas' }),
        ('Ricardo Alves Pereira', {'team': 'FC Dallas Reserves' }),
        ('Ricardo Alves Pereira', {'team': 'FC Tokyo' }),
        ('Ricardo Alves Pereira', {'team': 'Ponte Preta' }),
        ],

    'Ronaldo': [
        ('Cristiano Ronaldo', {'team': 'Manchester United' }),
        ('Ronaldo Luís Nazário de Lima', {'team': 'AC Milan' }),
        ('Ronaldo Luís Nazário de Lima', {'team': 'Inter Milan' }),
        ],

    'Tiago': [
        ('Tiago Calvano', {'team': 'Minnesota United FC' }),

        ('Tiago Jorge Honório', {'team': 'Shenzhen Ruby'}),
        ('Tiago Jorge Honório', {'team': 'Shanghai United FC'}),
        ('Tiago Jorge Honório', {'team': 'Beijing Guoan'}),

        ('Tiago Mendes', {'team': 'Chelsea'}),
        ('Tiago Mendes', {'team': 'SL Benfica'}),
        ('Tiago Mendes', {'team': 'Braga'}),
        ],

    'Thiago': [
        ('Thiago de Souza', {'team': 'LA Galaxy' }),
        ('Thiago da Rosa Correa', {'team': 'Chicago Fire' }),
        ('Thiago da Rosa Correa', {'team': 'Chicago Fire Reserves' }),
        ],

    'Silvinho': [
        ('Silvio Paiva', {'team': 'Internacional', 'season': '1985' }),
        ('Silvio Paiva', {'team': 'Internacional', 'season': '1984' }),
        ('Silvio Paiva', {'team': 'Internacional', 'season': '1983' }),
        ('Silvio Paiva', {'team': 'Internacional', 'season': '1982' }),
        ('Silvio Paiva', {'team': 'Internacional', 'season': '1981' }),

        ],


    'Washington': [

        ('Washington Cerqueira', {'team': 'Sao Paulo FC', 'season': '2010',}),
        ('Washington Cerqueira', {'team': 'Sao Paulo FC', 'season': '2009',}),
        ('Washington Cerqueira', {'team': 'Fluminense', 'season': '2008',}),
        ('Washington Cerqueira', {'team': 'Urawa Red Diamonds', 'season': '2007',}),
        ('Washington Cerqueira', {'team': 'Ponte Preta', 'season': '2001',}),
        ('Washington Cerqueira', {'team': 'Ponte Preta', 'season': '2000',}),

        ('Washington Luiz Mascarenhas Silva', {'team': 'Ceara', 'season': '2011'}),
        ('Washington Luiz Mascarenhas Silva', {'team': 'Ceara', 'season': '2010'}),
        ('Washington Luiz Mascarenhas Silva', {'team': 'Portuguesa', 'season': '2008'}),
        ('Washington Luiz Mascarenhas Silva', {'team': 'SC Recife', 'season': '2007'}),
        ('Washington Luiz Mascarenhas Silva', {'team': 'Palmeiras', 'season': '2006'}),
        ('Washington Luiz Mascarenhas Silva', {'team': 'Palmeiras', 'season': '2005'}),
        
        ('Washington César Santos', {'team': 'Botafogo', 'season': '1990',}),
        ('Washington César Santos', {'team': 'Club Guarani', 'season': '1989',}),
        ('Washington César Santos', {'team': 'Fluminense', 'season': '1988',}),
        ('Washington César Santos', {'team': 'Fluminense', 'season': '1987',}),
        ('Washington César Santos', {'team': 'Fluminense', 'season': '1986',}),
        ('Washington César Santos', {'team': 'Fluminense', 'season': '1985',}),
        ('Washington César Santos', {'team': 'Fluminense', 'season': '1984',}),
        ('Washington César Santos', {'team': 'Atletico Paranaense', 'season': '1983',}),
        ('Washington César Santos', {'team': 'Galicia', 'season': '1981',}),

        ],

    }


sep_teams = {
    'Saint Louis': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Saint Louis University')],
    'Maryland': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Maryland')],
    'West Chester': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'West Chester University')],

    'CCNY': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'City College of New York')],
    'Stanford': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Stanford University')],
    'Furman': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Furman University')],
    'Coastal Carolina': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Coastal Carolina University')],
    'Virginia': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Virginia')],
    'UCF': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Central Florida')],

    'Loyola Chicago': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Loyola University Chicago')],
    'West Virginia': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'West Virginia University')],
    'Akron': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Akron')],
    'North Carolina': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'UNC Chapel Hill')],
    'Creighton': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Creighton University')],
    'South Florida': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of South Florida')],
    'New Mexico': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of New Mexico')],

    'UMBC': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Maryland Baltimore County')],
    'Michigan': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Michigan')],

    'VCU': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Virginia Commonwealth University')],
    'George Mason': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'George Mason University')],
    'Penn': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Pennsylvania')],

    'Pennsylvania': [
        (from_competition('Intercollegiate Association Football League'), 'University of Pennsylvania'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Pennsylvania'),
    ],




    'UVA': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Virginia')],
    'CSU Northridge': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'California State University, Northridge')],
    'Brockport State': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'SUNY Brockport')],
    'Howard': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Howard University')],
    'Cortland State': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'SUNY Cortland')],
    'Colgate': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Colgate University')],
    'Liberty': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Liberty University')],
    'Brown': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Brown University')],
    'Western Illinois': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Western Illinois University')],
    'Northern Illinois': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Northern Illinois University')],
    'Dartmouth': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Dartmouth College')],
    'Elon': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Elon University')],
    'Florida Gulf Coast': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Florida Gulf Coast University')],
    'Bradley': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Bradley University')],
    'Xavier': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Xavier University')],
    'Northwestern': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Northwestern University')],
    'South Carolina': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of South Carolina')],
    'Stony Brook': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'SUNY Stony Brook')],
    'Monmouth': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Monmouth University')],
    'Georgia State': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Georgia State University')],
    'St. John\'s': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'St. John\'s University')],
    'James Madison': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'James Madison University')],
    'Louisville': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Louisville')],

    'Lafayette': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Lafayette College')],
    'Air Force': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Air Force Academy')],

    'Kentucky': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Kentucky')],

    'Cornell': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Cornell University'),
        (from_competition('Intercollegiate Association Football League'), 'Cornell University'),
    ],

    'Niagara': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Niagara University')],
    'Winthrop': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Winthrop University')],
    'Drexel': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Drexel University')],
    'Northeastern': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Northeastern University')],
    'Georgetown': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Georgetown University')],
    'Marquette': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Marquette University')],

    'Wisconsin': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Wisconsin')],
    'Quinnipiac': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Quinnipiac University')],
    'Navy': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Naval Academy')],
    'St. Francis (Brooklyn)': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'St. Francis College')],

    'Fairfield': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Fairfield University')],


    'Delaware': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Delaware')],


    'Saint Mary\'s': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Saint Mary\'s College of California')],



    'Academica': [
        (from_competition('Primeira Liga'), 'Académica de Coimbra'),
        ],


    'Aguila': [
        (from_competition('Salvadoran Primera División'), 'CD Aguila'),
        (from_competition('CONCACAF Champions League'), 'CD Aguila'),
        (from_competition('CONCACAF Cup Winners Cup'), 'CD Aguila'),
        (from_competition('Copa Interclubes UNCAF'), 'CD Aguila'),
        ],

    'Albany': [
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Albany Capitals'),
        ],

    'Albuquerque': [
        (from_seasons('USL First Division', set(['1997', '1998'])), 'Albuquerque Geckos'),
        ],



    'Alianza': [
        (from_competition('Salvadoran Primera División'), 'Alianza F.C.'),
        (from_competition('Copa Interclubes UNCAF'), 'Alianza F.C.'),
        ],

    'America': [
        (from_competition('Liga MX'), 'Club America'),
        (from_competition('Copa MX'), 'Club America'),
        (from_competition('North American SuperLiga'), 'Club America'),
        (from_competition('Interliga'), 'Club America'),
        (from_competition('Liga MX Liguilla'), 'Club America'),
        (from_competition('Categoría Primera A'), 'America de Cali'),
        (from_competition('Brasileirão'), 'América Futebol Clube'),
        (from_competition('Campeonato Mineiro'), 'América Futebol Clube'),
        #(from_competition('Campeonato Carioca'), 'América (RJ)'),
        ],

    'Anaheim': [
        (from_competition('Continental Indoor Soccer League'), 'Anaheim Splash'),
        ],


    'Ángeles': [
        (from_competition('Liga MX'), 'Ángeles de Puebla'),
        ],


    'Antigua': [
        (from_competition('Liga Nacional de Guatemala'), 'Antigua GFC')
        ],

    'Arizona': [
        (from_competition('World Indoor Soccer League'), 'Arizona Thunder'),
        (from_competition('Continental Indoor Soccer League'), 'Arizona Sandsharks'),
    ],


    'Arsenal': [
        (from_competition('Argentine Primera División'), 'Arsenal de Sarandi'),
        ],

    #'Atlanta': [
    #    (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
    #    ],

    'Atlanta': [
        (from_seasons('USL First Division', set(['1997'])), 'Atlanta Ruckus'),
        (from_seasons('American Professional Soccer League', set(['1995'])), 'Atlanta Ruckus'),
        ],


    'Atlético Nacional': [
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        ],

    'Athletic': [
        (from_competition('La Liga'), 'Atletico Madrid'),
        ],


    'Athletics': [
        (from_competition('North Texas Soccer Football League'), 'Dallas Athletics'),
        ],


    'Atletico': [
        (from_competition('La Liga'), 'Atletico Madrid'),
        (from_competition('Brasileirão'), 'Atlético Paranaense'),
        ],

    'Baltimore': [
        (from_competition('American League of Professional Football'), 'Baltimore Orioles'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Baltimore Blast'),
        (from_competition('North American Soccer League (indoor)'), 'Baltimore Comets'),
        (from_seasons('American Soccer League (1933-1983)', set(['1934-1935', '1945-1946'])), 'Baltimore Americans'),
        (from_seasons('American Soccer League (1933-1983)', set(['1936-1937', '1940-1941',])), 'Baltimore S.C.'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Baltimore Blast'),
        ],

    'Baltimore FC': [
        (from_seasons('American Soccer League (1933-1983)', set(['1937-1938', '1938-1939', '1939-1940', '1940-1941', '1941-1942',])), 'Baltimore S.C.'),
        ],


    'Barcelona': [
        (from_competition('La Liga'), 'FC Barcelona'),
        (from_competition('UEFA Super Cup'), 'FC Barcelona'),
        (from_competition('FIFA Club World Cup'), 'FC Barcelona'),
        (from_competition('UEFA Champions League'), 'FC Barcelona'),
        (from_competition('Ecuadorian Serie A'), 'Barcelona Sporting Club'),
        (from_competition('Copa Libertadores'), 'Barcelona Sporting Club'),
        ],


    'Benfica': [
        (from_competition('Jamaica National Premier League'), 'Benfica FC'),
        (from_competition('Primeira Liga'), 'SL Benfica'),
        (from_competition('Intercontinental Cup'), 'SL Benfica'),
        ],

    'Berlin': [
        (from_competition('1. Bundesliga'), 'Hertha BSC Berlin'),
        ],

    'Bensonhurst': [
        (from_competition('Field Club League'), 'Bensonhurst CFC'),
        ],


    'Bethlehem': [
        (from_competition('Allied American Foot Ball Association'), 'Bethlehem Steel'),
        (from_competition('American League (Philadelphia)'), 'Bethlehem Steel'),
        (from_competition('American Soccer League (1921-1933)'), 'Bethlehem Steel'),
        (from_seasons('American Soccer League (1933-1983)', set(['1938-1939'])), 'Bethlehem Hungarian'),
        (from_competition('U.S. Open Cup'), 'Bethlehem Steel'),
        (from_competition('Friendly'), 'Bethlehem Steel'),

        ],

    'Boston': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929 Fall'])), 'Boston Wonder Workers'),
        (from_seasons('American Soccer League (1921-1933)', set(['1929-1930', ])), 'Boston Bears'),
        (from_seasons('American Soccer League (1921-1933)', set(['1931 Spring', '1931 Fall', '1932 Spring', '1932 Fall'])), 'Boston Bears'),
        (from_seasons('American Soccer League (1933-1983)', set(['1934-1935'])), 'Boston Bears'),
        (from_seasons('American Soccer League (1933-1983)', set(['1969'])), 'Boston Astros'),
        (from_competition('North American Soccer League (indoor)'), 'Boston Minutemen'),
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Boston Bolts'),
        (from_seasons('USL First Division', set(['1999',])), 'Boston Bulldogs'),
        ],

    'Boston SC': [
        (from_seasons('American Soccer League (1933-1983)', set(['1963-1964'])), 'Boston Astros'),
        ],

    'Bohemians': [
        (from_competition('Gambrinus Liga'), 'Bohemians 1905'),
        ],

    'Bridgeport': [
        (from_seasons('American Soccer League (1921-1933)', set(['1929 Fall'])), 'Bridgeport Bears'),
        (from_seasons('American Soccer League (1921-1933)', set(['1929-1930'])), 'Bridgeport Hungaria'),
        ],


    'British-American': [
        (from_competition('Schmelzer Cup'), 'British-American (Kansas City)'),
        ],


    'Brooklyn': [
        (from_seasons('American Soccer League (1921-1933)', set(['1922-1923', '1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929 Fall', '1929-1930', '1930 Fall', '1931 Spring',])), 'Brooklyn Wanderers'),
        ],

    'Brooklyn FC': [
        (from_seasons('American Soccer League (1933-1983)', set(['1924-1925', '1928-1929'])), 'Brooklyn St. Mary\'s Celtic'),
        ],


    'Brooklyn Celtic': [
        (from_competition('American Soccer League (1933-1983)'), 'Brooklyn St. Mary\'s Celtic'),
        (from_seasons('US Open Cup', set([1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1942])), 'Brooklyn St. Mary\'s Celtic'),
        ],

    'Brooklyn Hakoah': [
        (from_competition('American Soccer League (1933-1983)'), 'Hakoah (ASL2)'),
        ],


    'Brooklyn Wanderers': [
        (from_seasons('American Soccer League (1933-1983)', set(['1942-1943', '1943-1944', '1944-1945', '1945-1946', '1946-1947', '1947-1948', '1948-1949', ])),
         'Brooklyn Wanderers (ASL2)'), # Sold and became Brooklyn Hakaoh
        ],


    'Buenos Aires': [
        (from_competition('Primera División de Costa Rica'), 'Buenos Aires (Costa Rica)'),
        ],


    'Buffalo': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Buffalo Stallions'),
        ],



    'CAI': [
        (from_competition('Liga Panameña de Fútbol'), 'CAI de La Chorrera'),
        ],


    'Calgary': [
        (from_competition('North American Soccer League (indoor)'), 'Calgary Boomers'),
        (from_competition('Western Soccer League'), 'Calgary Kickers'),
        ],

    'California': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of California, Berkeley'),
        (from_competition('North American Soccer League (indoor)'), 'California Surf'),
        (from_seasons('USL First Division', set(['1997','1998'])), 'California Jaguars'),
        ],


    'Cardiff': [
        (from_competition('Premier League'), 'Cardiff City'),
        ],

    'Carolina': [
        (from_seasons('USL First Division', set(['1997'])), 'Carolina Dynamo'),
        (from_competition('Continental Indoor Soccer League'), 'Carolina Vipers'),
        ],

    'Cartagena': [
        (from_competition('Categoría Primera A'), 'Real Cartagena'),
        ],

    'Celtic': [
        (from_competition('Intercontinental Cup'), 'Glasgow Celtic'),
        ],


    'Central': [
        (from_competition('Uruguayan Primera División'), 'Central Español'),
        ],

    'Chaco': [
        (from_competition('Liga de Fútbol Profesional Boliviano'), 'Chaco Petrolero'),
        ],

    'Charleston': [
        (from_seasons('USL First Division', set(['1997', '1998', '1999','2001', '2002','2003'])), 'Charleston Battery'),
        ],

    'Charlotte': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'UNC Charlotte'),
        (from_seasons('USL First Division', set(['2001','2002'])), 'Charlotte Eagles'),
        ],

    'Chicago': [
        (from_competition('Major League Soccer'), 'Chicago Fire'),
        (from_competition('North American Soccer League (indoor)'), 'Chicago Sting'),
        (from_seasons('Major Indoor Soccer League (1978-1992)', set(['1982-1983', '1984-1985', '1985-1986', '1986-1987', '1987-1988'])), 'Chicago Sting'),
        (from_seasons('Major Indoor Soccer League (1978-1992)', set(['1980-1981'])), 'Chicago Horizon'),

        (from_seasons('Major Indoor Soccer League (2008-2014)', set(['2012-2013'])), 'Chicago Soul'),
        (from_seasons('Major Indoor Soccer League (2008-2014)', set(['2010-2011'])), 'Chicago Riot'),

        ],

    'Chicago Fire': [
        (from_competition('USL Premier Developmental League'), 'Chicago Fire (PDL)'),
        ],

    'Cincinnati': [
        (from_seasons('USL First Division', set(['1998','1999',])), 'Cincinnati Riverhawks'),
        ],


    'Cleveland': [
        (from_seasons('Major Indoor Soccer League (1978-1992)', set(['1978-1979', '1979-1980', '1980-1981', '1981-1982', '1982-1983', '1983-1984', '1984-1985', '1985-1986', '1986-1987', '1987-1988'])), 'Cleveland Force'),
        (from_seasons('Major Indoor Soccer League (1978-1992)', set(['1989-1990', '1990-1991', '1991-1992'])), 'Cleveland Crunch'),
        ],


    'Colorado': [
        (from_competition('Major League Soccer'), 'Colorado Rapids'),
        (from_seasons('USL First Division', set(['1997'])), 'Colorado Foxes'),
        (from_seasons('American Professional Soccer League', set(['1994', '1995','1996'])), 'Colorado Foxes'),        
        ],


    'Columbus': [
        (from_competition('Major League Soccer'), 'Columbus Crew'),
        (from_competition('MLS Cup Playoffs'), 'Columbus Crew'),
        ],

    'Columbia': [
        (from_competition('New York State League'), 'Columbia Oval'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Columbia University'),
        ],


    'Connecticut': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Connecticut'),
        (from_seasons('USL First Division', set(['1997','1998','1999'])), 'Connecticut Wolves'),
        ],


    'Cristal': [
        (from_competition('Peruvian Primera División'), 'Sporting Cristal'),
        ],

    'CSKA': [
        (from_competition('Russian Premier League'), 'CSKA Moscow'),
        ],

    'Dacia': [
        (from_competition('Liga I'), 'CS Mioveni'),
        ],

    'Dallas': [
        (from_competition('Continental Indoor Soccer League'), 'Dallas Sidekicks'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Dallas Sidekicks'),
        (from_competition('World Indoor Soccer League'), 'Dallas Sidekicks'),
        (from_competition('North American Soccer League (indoor)'), 'Dallas Tornado'),
        ],


    'Denver': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Denver'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Denver Avalanche'),
        ],



    'Detroit': [
        (from_competition('Continental Indoor Soccer League'), 'Detroit Neon'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Detroit Lightning'),
        (from_competition('North American Soccer League (indoor)'), 'Detroit Express'),
        ],

    'Deportivo': [
        (from_competition('La Liga'), 'Deportivo La Coruna'),
        (from_competition('Ecuadorian Serie A'), 'Deportivo Quevedo'),
        ],


    'Dinamo': [
        (from_competition('Liga I'), 'Dynamo Bucharest'),
        (from_competition('Russian Premier League'), 'Dynamo Moscow'),
        ],


    'Doncaster': [
        (from_competition('Women\'s Premier League'), 'Doncaster Belles'),
        ],


    'Doncaster Rovers': [
        (from_competition('Women\'s Premier League'), 'Doncaster Belles'),
        ],



    'Dynamo': [
        (from_competition('North American SuperLiga'), 'Houston Dynamo'),
        (from_competition('Major League Soccer'), 'Houston Dynamo'),
        (from_competition('CONCACAF Champions League'), 'Houston Dynamo'),
        ],

    'Edmonton': [
        (from_competition('North American Soccer League (indoor)'), 'Edmonton Drillers'),
        ],

    'El Paso': [
        (from_seasons('USL First Division', set(['1997','1998','1999', '2000', '2001', '2002'])), 'El Paso Patriots'),
        ],

    'España': [
        (from_competition('Liga Nacional de Honduras'), 'Real C.D. España'),
        ],

    'Estudiantes': [
        (from_competition('Liga MX'), 'Tecos'),
        (from_competition('Copa MX'), 'Tecos'),
        (from_competition('InterLiga'), 'Tecos'),
        (from_competition('Ascenso MX'), 'Tecos'),
        (from_competition('Copa Libertadores'), 'Estudiantes de La Plata'),
        (from_competition('Copa Sudamericana'), 'Estudiantes de La Plata'),
        (from_competition('Argentine Primera División'), 'Estudiantes de La Plata'),
        (from_competition('Peruvian Primera División'), 'Estudiantes Grau'),
        (from_competition('Venezuelan Primera División'), 'Estudiantes de Mérida'),
        ],


    'Fall River': [
        (from_seasons('American Soccer League (1921-1933)', set(['1922-1923', '1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929-1930', '1929 Fall', '1930 Spring', '1930 Fall'])), 'Fall River Marksmen'),
        (from_seasons('American Soccer League (1921-1933)', set(['1931 Spring', '1932 Fall'])), 'Fall River FC'), 
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922'])), 'Fall River Rovers'),
        (from_seasons('American Soccer League (1933-1983)', set(['1959-1960', '1960-1961', '1961-1962', '1962-1963', '1963-1964',])), 'Fall River SC'),
        ],

    'Fall River': [
        (from_seasons('American Soccer League (1933-1983)', set(['1957-1958'])), 'Fall River SC'),
        ],

    'Fort Lauderdale': [
        (from_competition('North American Soccer League (indoor)'), 'Fort Lauderdale Strikers'),
        (from_seasons('American Professional Soccer League', set(['1989', '1990', '1994'])), 'Fort Lauderdale Strikers'),
        ],


    'Federal': [
        (from_competition('Liga Nacional de Honduras'), 'Federal (Honduras)'),
        ],


    'Fortuna': [
        (from_competition('Eredivisie'), 'Fortuna Sittard'),
        ],

    'Gimnàstic': [
        (from_competition('La Liga'), 'Gimnàstic de Tarragona'),
        ],

    'Gimnasia y Esgrima': [
        (from_competition('Copa Libertadores'), 'Gimnasia y Esgrima La Plata'),
        (from_competition('Copa Sudamericana'), 'Gimnasia y Esgrima La Plata'),
        ],

    'GC': [
        (from_competition('Swiss Super League'), 'Grasshopper Club'),
        ],

    'Golden Bay': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Golden Bay Earthquakes'), 
        ],


    'Hakoah': [
        (from_seasons('American Soccer League (1921-1933)', set(['1929-1930', '1930 Spring', '1930 Fall', '1931 Spring', '1931 Fall', '1932 Spring',])), 'Hakoah All-Stars'),
        (from_seasons('American Soccer League (1921-1933)', set(['1929 Fall',])), 'Brooklyn Hakoah'),
        (from_competition('Eastern Soccer League (1928-1929)'), 'New York Hakoah'),
        (from_competition('American Soccer League (1933-1983)'), 'Hakoah (ASL2)'),

        ],

    'Hampton Roads': [
        (from_seasons('USL First Division', set(['1997','1998','1999'])), 'Hampton Roads Mariners'),
        ],


    'Harrison': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922', '1922-1923', '1923-1924'])), 'Harrison SC'),
        ],


    'Harrisville': [
        (from_competition('Times Cup'), 'Harrisvile (RI)'),
        ],


    'Hartford': [
        (from_seasons('American Soccer League (1921-1933)', set(['1927-1928'])), 'Hartford Americans'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Hartford Hellions'),
        (from_competition('North American Soccer League (indoor)'), 'Hartford Bicentennials'),
        ],

    'Hamilton': [
        (from_competition('Scottish Premier League'), 'Hamilton Academical'),
        ],

    'Heredia': [
        (from_competition('Liga Nacional de Guatemala'), 'Heredia Jaguares de Peten'),
        (from_competition('Primera División de Costa Rica'), 'CS Herediano'),
        ],

    'Hershey': [
        (from_seasons('USL First Division', set(['1997', '1998','1999' ])), 'Hershey Wildcats'),
        ],


    'Hispano': [
        (from_competition('American Soccer League (1933-1983)'), 'Brooklyn Hispano'),
        (from_competition('Liga Nacional de Honduras'), 'Hispano (Comayagua)'),
        ],

    'Holyoke': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922'])), 'Holyoke Falcos'),
        ],


    'Huelva': [
        (from_competition('La Liga'), 'Recreativo Huelva'),
        ],



    'Hollywood': [
        (from_competition('New York Amateur League'), 'Hollywood Inn'),
        ],


    'Houston': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Houston Summit'),
        (from_competition('Continental Indoor Soccer League'), 'Houston Hotshots'),
        (from_competition('World Indoor Soccer League'), 'Houston Hotshots'),
        (from_competition('Major League Soccer'), 'Houston Dynamo'),
        ],

    'Hungaria': [
        (from_seasons('Eastern Soccer League (1928-1929)', set(['1928-1929 Second Half'])), 'New York Hungaria'),
        #(from_seasons('Eastern Soccer League (1928-1929)', set(['1929 Fall'])), 'Victoria Hungaria'),
        (from_seasons('Eastern Soccer League (1928-1929)', set(['1929 Fall'])), 'New York Hungaria'), # the same, apparently.
        (from_seasons('American Soccer League (1921-1933)', set(['1929-1930'])), 'Bridgeport Hungaria'),
        ],

    'Indiana': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1926-1927'])), 'Indiana Flooring'),
        (from_competition('Continental Indoor Soccer League'), 'Indiana Twisters'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Indiana University'),
        (from_seasons('USL First Division', set(['1999',])), 'Indiana Blast'),
        ],

    'Indianapolis': [
        (from_competition('Continental Indoor Soccer League'), 'Indiana Twisters'),
        ],

    'Irish Americans': [
        (from_competition('American Soccer League (1933-1983)'), 'Kearny Celtic'),
        ],

    'Jersey City': [
        (from_competition('American Soccer League (1921-1933)'), 'Jersey City (ASL)'),
        ],

    'Jacksonville': [
        (from_competition('North American Soccer League (indoor)'), 'Jacksonville Tea Men'),
        (from_seasons('USL First Division', set(['1997', '1998', '1999'])), 'Jacksonville Cyclones'),
        ],

    'Junior': [
        (from_competition('Categoría Primera A'), 'Junior de Barranquilla'),
        ],

    'Juventud': [
        (from_competition('Liga Nacional de Honduras'), 'Real Juventud'),
        (from_competition('Uruguayan Primera División'), 'Juventud de Las Piedras'),
        ],


    'Kansas City': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Kansas City Comets'),
        ],

    'Las Vegas': [
        (from_competition('Continental Indoor Soccer League'), 'Las Vegas Dustdevils'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Las Vegas Americans'),
        ],


    'Lehigh Valley': [
        (from_seasons('USL First Division', set(['1999',])), 'Lehigh Valley Steam'),
        ],



    'Liverpool': [
        (from_competition('Uruguayan Primera División'), 'Liverpool (Montevideo)'),
        ],

    'Lokomotiv': [
        (from_competition('Russian Premier League'), 'Lokomotiv Moscow'),
        ],

    'Long Island': [
        (from_seasons('USL First Division', set(['1997','1998','1999'])), 'Long Island Rough Riders'),
        ],


    'Los Andes': [
        (from_competition('Argentine Primera División'), 'Los Andes de Lomas de Zamora'),
        ],

    'Los Angeles': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Los Angeles Lazers'),
        (from_competition('North American Soccer League (indoor)'), 'Los Angeles Aztecs'),
        (from_competition('Continental Indoor Soccer League'), 'Los Angeles United'),
        (from_seasons('American Professional Soccer League', set(['1994'])), 'Los Angeles Salsa'),
        ],

    'Ludlow': [
        (from_seasons('American Soccer League (1921-1933)', set(['1956-1957'])), 'Ludlow Lusitano'),
        ],

    'Ludlow': [
        (from_seasons('American Soccer League (1921-1933)', set(['1956-1957', '1957-1958'])), 'Ludlow Lusitano'),
        ],


    'Marte': [
        (from_competition('Salvadoran Primera División'), 'C.D. Atlético Marte'),
        ],

    'Maryland': [
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Maryland Bays'),
        (from_seasons('USL First Division', set(['1999'])), 'Maryland Mania'),
        ],


    'Memphis': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Memphis Americans'),
        ],

    'Mérida': [
        (from_competition('Ascenso MX'), 'C.F. Mérida'),
        ],

    'Miami': [
        (from_competition('North American Soccer League (indoor)'), 'Miami Toros'),
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Miami Sharks'),
        ],

    'Milwaukee': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Wisconsin-Milwaukee'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Milwaukee Wave'),
        (from_seasons('USL First Division', set(['1997', '1998', '1999', '2000', '2001', '2002'])), 'Milwaukee Rampage'),
        ],


    'Minnesota': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Minnesota Strikers'),
        (from_competition('North American Soccer League (indoor)'), 'Minnesota Strikers'),
        (from_seasons('USL First Division', set(['1997', '1998', '1999', '2000', '2001', '2002', '2003'])), 'Minnesota Thunder'),
        ],


    'Missouri': [
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Missouri Comets'),
        ],

    'Monterrey': [
        (from_competition('Continental Indoor Soccer League'), 'Monterrey La Raza'),
        (from_competition('World Indoor Soccer League'), 'Monterrey La Raza'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Monterrey La Raza'),
        (from_competition('CONCACAF Champions\' Cup'), 'CF Monterrey'),
        (from_competition('CONCACAF Champions League'), 'CF Monterrey'),
        (from_competition('Copa Libertadores'), 'CF Monterrey'),
        (from_competition('Club World Cup'), 'CF Monterrey'),
        (from_competition('Liga MX'), 'CF Monterrey'),

        ],

    'Montreal': [
        (from_competition('Major League Soccer'), 'Montreal Impact'),
        (from_competition('MLS Cup Playoffs'), 'Montreal Impact'),
        (from_competition('North American Soccer League (indoor)'), 'Montreal Manic'),
        (from_seasons('USL First Division', set(['1997', '1998', '2002'])), 'Montreal Impact'),        
        (from_seasons('American Professional Soccer League', set(['1994', '1995', '1996'])), 'Montreal Impact'),
        ],


    'Nacional': [
        (from_competition('Paraguayan Primera División'), 'Club Nacional'),
        (from_competition('Categoría Primera A'), 'Atlético Nacional'),
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        (from_competition('Primeira Liga'), 'CD Nacional'),
        ],

    'Nashville': [
        (from_seasons('USL First Division', set(['1997', '1998', '2001'])), 'Nashville Metros'),
        ],


    'Necaxa': [
        (from_competition('Liga Nacional de Honduras'), 'CD Necaxa'),
        ],

    'Newark': [
        (from_competition('Eastern Soccer League (1928-1929)'), 'Newark Skeeters'),
        (from_seasons('American Soccer League (1921-1933)', set(['1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929-1930', '1930 Spring'])), 'Newark Skeeters'),
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Fall','1931 Spring','1931 Fall',])), 'Newark Americans'),
        ],

    'New Bedford': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929 Fall', '1929-1930', '1930 Spring', '1930 Fall', '1931', '1931 Spring', '1931 Fall', '1932 Spring'])), 'New Bedford Whalers'),
        ],


    'New England': [
        (from_competition('North American Soccer League (indoor)'), 'New England Tea Men'),
        (from_competition('Major League Soccer'), 'New England Revolution'),
        (from_competition('MLS Cup Playoffs'), 'New England Revolution'),

        ],


    'New Jerseyf': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'New Jersey Rockets'),
        (from_seasons('American Professional Soccer League', set(['1989'])), 'New Jersey Eagles'),
        ],

    'New Orleans': [
        (from_seasons('USL First Division', set(['1997', '1998','1999'])), 'New Orleans Riverboat Gamblers'),
        ],


    'New York': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922', '1922-1923', '1923-1924'])), 'New York Field Club'),
        (from_seasons('American Soccer League (1921-1933)', set(['1925-1926'])), 'New York Giants (1923-1930)'),
        (from_competition('North American Soccer League (indoor)'), 'New York Cosmos'),
        (from_seasons('Major Indoor Soccer League (1978-1992)',  set(['1978-1979', '1979-1980', '1980-1981', '1981-1982', '1982-1983', '1983-1984'])), 'New York Arrows'),
        (from_seasons('Major Indoor Soccer League (1978-1992)',  set(['1984-1985'])), 'New York Cosmos'),
        (from_seasons('Major Indoor Soccer League (1978-1992)',  set(['1986-1987'])), 'New York Express'),
        (from_seasons('American Professional Soccer League', set(['1995'])), 'New York Centaurs'),
        (from_seasons('American Professional Soccer League', set(['1996',])), 'New York Fever'),
        ],

    'New York City': [
        (from_competition('Major League Soccer'), 'New York City FC'),
        ],


    'New York Giants': [
        (from_competition('Eastern Soccer League (1928-1929)'), 'New York Giants (1923-1930)'),
        (from_seasons('American Soccer League (1921-1933)', set(['1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929-1930', '1930 Spring'])), 'New York Giants (1923-1930)'),
        (from_competition('American Soccer League (1921-1933) Playoffs'), 'New York Nationals'),
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Fall', '1931 Spring', '1931 Fall', '1932 Spring', '1932 Fall'])), 'New York Nationals'),
        ],


    'New York Hakoah': [
        (from_seasons('American Soccer League (1921-1933)', set(['1929-1930'])), 'Hakoah All-Stars'),
        (from_competition('American Soccer League (1933-1983)'), 'Hakoah (ASL2)'),
        ],

    'New York SC': [
        (from_seasons('American Soccer League (1921-1933)', set(['1923-1924','1930 Fall'])), 'New York Giants (1923-1930)'),
        ],

    'New York Soccer Club': [
        (from_seasons('American Soccer League (1921-1933)', set(['1923-1924','1930 Fall'])), 'New York Giants (1923-1930)'),
        ],


    'Nomads': [
        (from_competition('North Texas Soccer Football League'), 'Dallas Nomads'),
        ],


    'Norfolk': [
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Norfolk SharX'),
        ],


    'Olympia': [
        (from_competition('Illinois State Football Association 2nd Division'), 'Chicago Olympia'),
        ],


    'Olimpia': [
        (from_competition('CONCACAF Champions League'), 'CD Olimpia'),
        (from_competition('Copa Interclubes UNCAF'), 'CD Olimpia'),
        (from_competition('Copa Mercosur'), 'Club Olimpia'),
        (from_competition('Copa Libertadores'), 'Club Olimpia'),

        (from_competition('Liga I'), 'Olimpia Satu Mare'),

        (from_competition('Liga Nacional de Honduras'), 'CD Olimpia'),

        (from_competition('Paraguayan Primera División'), 'Club Olimpia'),
        (from_competition('Copa Libertadores'), 'Club Olimpia'), # right?

        (from_competition('Uruguayan Primera División'), 'Olimpia (Uruguay)'),

        ],

    'Omaha': [
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Omaha Vipers'),
        ],
    
    'Orange County': [
        (from_seasons('USL First Division', set(['1997','1998','1999'])), 'Orange County Blue Star'),
        ],

    'Orlando': [
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Orlando Lions'),
        (from_seasons('USL First Division', set(['1997'])), 'Orlando Sundogs'),
        (from_competition('Major League Soccer'), 'Orlando City FC'),
        ],

    'Paris': [
        (from_competition('Ligue 1'), 'Paris Saint-Germain'),
        ],

    'Paterson': [
        (from_seasons('American Soccer League (1921-1933)', set(['1922-1923',])), 'Paterson FC'),
        (from_seasons('American Soccer League (1933-1983)', set(['1939-1940', '1940-1941'])), 'Paterson FC (ASL2)'),
        ],


    'Paterson FC': [
        (from_seasons('American Soccer League (1933-1983)', set(['1938-1939', '1939-1940', '1940-1941'])), 'Paterson FC (ASL2)'),
        ],

    'Pawtucket': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922', '1922-1923', '1925-1926', '1928-1929', '1929 Fall', '1929-1930', '1930 Spring', '1930 Fall', '1931 Spring', '1931 Fall', '1932 Spring', '1932 Fall'])), 'Pawtucket Rangers'),
        ],


    'Paysandu': [
        (from_competition('Uruguayan Primera División'), 'Paysandu FC'),
        (from_competition('Copa Libertadores'), 'Paysandu Sport Club')
        ],

    'Penn-Jersey': [
        (from_seasons('American Professional Soccer League', set(['1990'])), 'Penn-Jersey Spirit'),
        ],


    'Philadelphia': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922', '1922-1923', '1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929 Fall'])), 'Philadelphia Field Club'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Philadelphia Fever'),
        (from_seasons('North American Soccer League (indoor)',  set(['1975', ])), 'Philadelphia Atoms'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Philadelphia KiXX'),
        (from_competition('Major League Soccer'), 'Philadelphia Union'),
        ],

    'Phoenix': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Phoenix Inferno'),
        ],


    'Platense': [
        (from_competition('CONCACAF Champions League'), 'Platense F.C.'),
        (from_competition('CONCACAF Cup Winners Cup'), 'Platense F.C.'),
        ],



    'Pittsburgh': [
        (from_competition('Continental Indoor Soccer League'), 'Pittsburgh Stingers'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Pittsburgh Spirit'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Pittsburgh'),
        (from_seasons('USL First Division', set(['1999', '2000', '2001',])), 'Pittsburgh Riverhounds'),
        ],



    'Portland': [
        (from_competition('Continental Indoor Soccer League'), 'Portland Pride'),
        (from_competition('World Indoor Soccer League'), 'Portland Pythons'),
        (from_competition('North American Soccer League (indoor)'), 'Portland Timbers'),
        (from_competition('Western Soccer League'), 'Portland Timbers'),
        (from_seasons('USL First Division', set(['2001','2002',])), 'Portland Timbers'),
        (from_competition('Major League Soccer'), 'Portland Timbers'),
        (from_competition('MLS Cup Playoffs'), 'Portland Timbers'),
        ],



    'Providence': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1929 Fall', '1929-1930', '1930 Spring', '1930 Fall'])), 'Providence Clamdiggers'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Providence College'),
        ],

    'Progreso': [
        (from_competition('Uruguayan Primera División'), 'CA Progreso'),
        (from_competition('Copa Libertadores'), 'CA Progreso'),
        ],


    'Rapid': [
        (from_competition('Liga I'), 'Rapid Bucureşti'),

        ],

    'Real Espana': [
        (from_competition('Liga Nacional de Honduras'), 'Real C.D. España'),
        (from_competition('CONCACAF Champions League'), 'Real C.D. España'),
        (from_competition('Copa Interclubes UNCAF'), 'Real C.D. España'),
        ],

    'Racing': [
        (from_competition('Liguilla Pre-Libertadores de América (Uruguay)'), 'Racing Club de Montevideo'),
        (from_competition('Uruguayan Primera División'), 'Racing Club de Montevideo'),
        (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
        (from_competition('La Liga'), 'Racing de Santander'),
        ],

    'Racing Club': [
        (from_competition('Liguilla Pre-Libertadores de América (Uruguay)'), 'Racing Club de Montevideo'),
        (from_competition('Uruguayan Primera División'), 'Racing Club de Montevideo'),
        (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
        (from_competition('Campeonato Metropolitano (Argentina)'), 'Racing Club de Avellaneda'),        
        ],

    'Raleigh': [
        (from_seasons('USL First Division', set(['1997','1998','1999'])), 'Raleigh Flyers'),
        ],


    'Rangers': [
        (from_competition('Chilean Primera División'), 'Rangers de Talca'),
        (from_competition('Scottish Premier League'), 'Glasgow Rangers'),
        (from_competition('UEFA Champions League'), 'Glasgow Rangers'),
        (from_competition('UEFA Europa League'), 'Glasgow Rangers'),
        (from_competition('Scottish League Cup'), 'Glasgow Rangers'),
        ],

    'Rapid': [
        (from_competition('Austrian Bundesliga'), 'Rapid Vienna'),
        ],

    'Recreativo': [
        (from_competition('La Liga'), 'Recreativo Huelva'),
        ],

    'Richmond': [
        (from_seasons('USL First Division', set(['1997', '1998', '1999','2002'])), 'Richmond Kickers'),
        ],



    'River Plate': [
        (from_competition('Uruguayan Primera División'), 'River Plate (Montevideo)'),
        ],

    'River': [
        (from_competition('Uruguayan Primera División'), 'River Plate (Montevideo)'),
        ],

    'Rochester': [
        (from_competition('North American Soccer League (indoor)'), 'Rochester Lancers'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Rochester Lancers'),
        (from_seasons('American Professional Soccer League', set(['1996',])), 'Rochester Rhinos'),
        (from_seasons('USL First Division', set(['1997','1998','1999','2000','2001','2002','2003'])), 'Rochester Rhinos'),
        ],


    'Rockford': [
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Rockford Rampage'),
        ],



    'Sacachispas': [
        (from_competition('Liga Nacional de Guatemala'), 'CSD Sacachispas')
        ],

    'Sacramento': [
        (from_competition('Continental Indoor Soccer League'), 'Sacramento Knights'),
        (from_competition('World Indoor Soccer League'), 'Sacramento Knights'),
        (from_seasons('USL First Division', set(['1999'])), 'Sacramento Geckos'),
        ],


    'Salzburg': [
        (from_competition('Liga Nacional de Honduras'), 'Honduras Salzburg'),
        ],

    'San Diego': [
        (from_competition('Continental Indoor Soccer League'), 'San Diego Sockers'),
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'San Diego Sockers'),
        (from_competition('World Indoor Soccer League'), 'San Diego Sockers'),
        (from_competition('North American Soccer League (indoor)'), 'San Diego Sockers'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of San Diego'),
        (from_seasons('USL First Division', set(['1998','1999','2001','2002',])), 'San Diego Flash'),
        ],

    'San Francisco': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'San Francisco Fog'),
        (from_competition('Liga Panameña de Fútbol'), 'San Francisco FC'),
        (from_competition('Copa Interclubes UNCAF'), 'San Francisco FC'),
        (from_competition('CONCACAF Champions League'), 'San Francisco FC'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of San Francisco'),
        ],

    'San Francisco Bay': [
        (from_seasons('American Professional Soccer League', set(['1990',])), 'San Francisco Bay Blackhawks'),
        (from_seasons('USL First Division', set(['1998','1999'])), 'San Francisco Bay Seals'),
        ],

    'San Jose': [
        (from_competition('Liga de Fútbol Profesional Boliviano'), 'CD San José',),
        (from_competition('Continental Indoor Soccer League'), 'San Jose Grizzlies'),
        (from_competition('North American Soccer League (indoor)'), 'San Jose Earthquakes'),
        (from_competition('Major League Soccer'), 'San Jose Earthquakes'),
        ],

    'San Jose Earthqukaes': [
        (from_competition('USL Premier Developmental League'), 'San Jose Earthquakes (PDL)'),
        ],
        


    'San Marcos': [
        (from_competition('Nicaraguan Primera División'), 'FC San Marcos'),
        (from_competition('Chilean Primera División'), 'San Marcos de Arica'),

        ],

    'Santa Fe': [
        (from_competition('Categoría Primera A'), 'Independiente Santa Fe'),
        (from_competition('Copa Libertadores'), 'Independiente Santa Fe'),
        ],

    'Santa Lucia': [
        (from_competition('Liga Nacional de Guatemala'), 'Santa Lucía Cotzumalguapa'),
        ],


    'Santa Barbara': [
        (from_competition('Primera División de Costa Rica'), 'Santa Barbara (Costa Rica)'),
        ],


    'San Lorenzo': [
        (from_competition('Paraguayan Primera División'), 'Sportivo San Lorenzo'),
        (from_competition('Copa Libertadores'), 'San Lorenzo de Almagro'),
        (from_competition('Copa Mercosur'), 'San Lorenzo de Almagro'),
        ],


    'Santos': [
        (from_competition('Liga MX'), 'Santos Laguna'),
        (from_competition('CONCACAF Champions League'), 'Santos Laguna'),
        (from_competition('Copa MX'), 'Santos Laguna'),
        (from_competition('Liga MX Liguilla'), 'Santos Laguna'),
        (from_competition('Interliga'), 'Santos Laguna'),
        (from_competition('North American SuperLiga'), 'Santos Laguna'),
        (from_competition('Primera División de Costa Rica'), 'Santos de Guápiles'),
        (from_competition('Brasileirão'), 'Santos FC'),
        (from_competition('Copa Libertadores'), 'Santos FC'),
        (from_competition('Recopa Sudamericana'), 'Santos FC'),
        (from_competition('Copa Sudamericana'), 'Santos FC'),
        (from_competition('Copa CONMEBOL'), 'Santos FC'),
        ],


    'Seattle': [
        (from_competition('Major League Soccer'), 'Seattle Sounders'),
        (from_competition('MLS Cup Playoffs'), 'Seattle Sounders'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Seattle University'),
        (from_competition('Continental Indoor Soccer League'), 'Seattle SeaDogs'),
        (from_competition('North American Soccer League (indoor)'), 'Seattle Sounders'),
        (from_seasons('USL First Division', set(['1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003'])), 'Seattle Sounders'),
        (from_seasons('American Professional Soccer League', set(['1994','1995','1996'])), 'Seattle Sounders'),

        ],


    'Seoul': [
        (from_competition('K League'), 'FC Seoul'),
        ],


    'Shamrocks': [
        (from_competition('Western Missouri-Kansas Soccer Football Association'), 'Shamrock FC (Kansas City)'),
        ],

    'Shamrock FC': [
        (from_competition('Schmelzer Cup'), 'Shamrock FC (Kansas City)'),
        ],

    'Shawsheen': [
        (from_competition('American Soccer League (1921-1933)'), 'Shawsheen Indians'),
        ],


    'Springfield': [
        (from_competition('American Soccer League (1921-1933)'), 'Shawsheen Indians'),
        ],


    'Slavia': [
        (from_competition('Gambrinus Liga'), 'Slavia Prague'),
        (from_competition('UEFA Champions League'), 'Slavia Prague'),
        ],

    'Sociedad': [
        (from_competition('La Liga'), 'Real Sociedad'),
        ],

    'Sons of St. George': [
        (from_competition('Southern California Soccer League'), 'Los Angeles Sons of St. George'),
        ],


    'Sparta': [
        (from_competition('Illinois State Football Association 3rd Division'), 'Chicago Sparta'),
        (from_competition('Eredivisie'), 'Sparta Rotterdam'),
        (from_competition('Gambrinus Liga'), 'Sparta Prague'),
        ],

    'Sport': [
        (from_competition('Copa Libertadores'), 'SC Recife'),
        (from_competition('Brasileirão'), 'SC Recife'),
        ],

    'Sporting': [
        (from_competition('Liga Panameña de Fútbol'), 'Sporting San Miguelito'),
        (from_competition('Primeira Liga'), 'Sporting CP'),
        (from_competition('UEFA Champions League'), 'Sporting CP'),
        (from_competition('UEFA Europa League'), 'Sporting CP'),
        (from_competition('La Liga'), 'Sporting de Gijon'),
        ],

    'Springfield': [
        (from_competition('American Soccer League (1921-1933)'), 'Springfield Babes'),
        ],


    'St. Louis': [
        (from_competition('World Indoor Soccer League'), 'St. Louis Steamers'),
        (from_competition('North American Soccer League (indoor)'), 'St. Louis Stars'),
        (from_seasons('Major Indoor Soccer League (1978-1992)',  set(['1979-1980', '1980-1981', '1981-1982', '1982-1983', '1983-1984', '1984-1985', '1985-1986', '1986-1987', '1987-1988'])), 'St. Louis Steamers'),
        (from_seasons('Major Indoor Soccer League (1978-1992)',  set(['1989-1990', '1990-1991', '1991-1992'])), 'St. Louis Storm'),
        ],


    'Standard': [
        (from_competition('Belgian Pro League'), 'Standard Liège'),
        ],

    'Staten Island': [
        (from_seasons('USL First Division', set(['1998','1999',])), 'Staten Island Vipers'),
        (from_competition('Field Club Soccer League'), 'Staten Island C&TC'),
        ],

    'Staten Island FC': [
        (from_competition('Field Club Soccer League'), 'Staten Island C&TC'),
        ],

    'St. George\'s': [
        (from_competition('Western Missouri-Kansas Soccer Football Association'), 'St. George FC (Kansas City)'),
        ],

    'St. George F.C.': [
        (from_competition('Schmelzer Cup'), 'St. George FC (Kansas City)'),
        ],


    'Sturm': [
        (from_competition('Austrian Bundesliga'), 'Sturm Graz'),
        ],

    'Syracuse': [
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Syracuse Silver Knights'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'Syracuse University'),
        ],




    'Tacoma': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Tacoma Stars'),
        ],


    'Talleres': [
        (from_competition('Copa Libertadores'), 'Talleres de Córdoba',),
        (from_competition('Copa Mercosur'), 'Talleres de Córdoba',),
        ],


    'Tampa': [
        (from_competition('North American Soccer League (indoor)'), 'Tampa Bay Rowdies'),
        ],


    'Tampa Bay': [
        (from_competition('North American Soccer League (indoor)'), 'Tampa Bay Rowdies'),
        (from_seasons('American Professional Soccer League', set(['1989', '1990'])), 'Tampa Bay Rowdies'),
        ],

    'Tennessee': [
        (from_seasons('USL First Division', set(['1999'])), 'Tennessee Rhythm'),
        ],


    'Tigers': [
        (from_competition('Western Missouri-Kansas Soccer Football Association'), 'Shamrock FC (Kansas City)'),
        ],

    'Tiger FC': [
        (from_competition('Schmelzer Cup'), 'Tiger FC (Kansas City)'),
        ],


    'Todd': [
        (from_seasons('American Soccer League (1921-1933)', set(['1921-1922'])), 'Todd Shipyards'),
        ],

    'Toronto': [
        (from_competition('North American Soccer League (indoor)'), 'Toronto Blizzard'),
        (from_seasons('American Professional Soccer League', set(['1994'])), 'Toronto Rockets'),
        (from_seasons('USL First Division', set(['1997', '1998', '1999'])), 'Toronto Lynx'),
        ],

    'Tulsa': [
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Tulsa'),
        (from_competition('North American Soccer League (indoor)'), 'Tulsa Roughnecks'),
        ],



    'Tranmere': [
        (from_competition('FA Women\'s Premier League'), 'Tranmere Rovers Ladies'),
        ],

    'Tranmere Rovers': [
        (from_competition('FA Women\'s Premier League'), 'Tranmere Rovers Ladies'),
        ],



    'UCD': [
        (from_competition('League of Ireland'), 'University College Dublin'),
        ],

    'Universidad': [
        (from_competition('Liga Nacional de Honduras'), 'Pumas UNAH'),
        (from_competition('Liga Nacional de Guatemala'), 'Universidad de San Carlos'),
        ],

    'Universidad Católica': [
        (from_competition('Ecuadorian Serie A'), 'Universidad Católica del Ecuador'),
        ],

    'Union': [
        (from_competition('Argentine Primera División'), 'Unión de Santa Fe'),
        ],


    'Utah': [
        (from_competition('World Indoor Soccer League'), 'Utah Freezz'),
        ],

    'Valencia': [
        (from_competition('Liga Nacional de Honduras'), 'Municipal Valencia'),
        (from_competition('La Liga'), 'Valencia CF'),
        (from_competition('UEFA Super Cup'), 'Valencia CF'),

        ],

    'Vancouver': [
        (from_competition('Major League Soccer'), 'Vancouver Whitecaps'),
        (from_competition('MLS Cup Playoffs'), 'Vancouver Whitecaps'),
        (from_competition('North American Soccer League (indoor)'), 'Vancouver Whitecaps'),
        (from_competition('Western Soccer League'), 'Vancouver Whitecaps'), # i suspect
        (from_seasons('USL First Division', set(['1997'])), 'Vancouver 86ers'),        
        (from_seasons('USL First Division', set(['1998', '1999', '2000', '2001', '2002'])), 'Vancouver Whitecaps'),        
        (from_seasons('American Professional Soccer League', set(['1994', '1995','1996'])), 'Vancouver Whitecaps'),
        ],


    'Victoria': [
        (from_competition('Liga Nacional de Honduras'), 'CD Victoria'),
        ],


    'Victoria': [
        (from_competition('Liga Nacional de Honduras'), 'CDS Vida'),
        ],


    'Viking': [
        (from_competition('Tippeligaen'), 'Viking FK'),
        ],

    'Vitoria': [
        (from_competition('Brasileirão'), 'EC Vitória'),
        (from_competition('Copa CONMEBOL'), 'EC Vitória'),
        ],


    'Vitória FC': [
        (from_competition('Primeira Liga'), 'Vitória de Setúbal'),
        ],


    'Vitória SC': [
        (from_competition('Primeira Liga'), 'Vitória de Guimarães'),
        ],

    'Wanderers': [
        (from_competition('Uruguayan Primera División'), 'Montevideo Wanderers'),
        (from_competition('Chilean Primera División'), 'Santiago Wanderers'),
        (from_competition('Chicago Foot Ball Association'), 'Chicago Wanderers'),
        (from_competition('Southern California Soccer League'), 'Los Angeles Wanderers'),
        ],

    'Washington': [
        (from_competition('Continental Indoor Soccer League'), 'Washington Warthogs'),
        (from_competition('North American Soccer League (indoor)'), 'Washington Diplomats'),
        (from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Washington'),
        ],


    'Wichita': [
        (from_competition('Major Indoor Soccer League (1978-1992)'), 'Wichita Wings'),
        (from_competition('Major Indoor Soccer League (2008-2014)'), 'Wichita Wings'),
        ],

    'Worcester': [
        (from_seasons('USL First Division', set(['1997', '1998'])), 'Worcester Wildfire')
        ],

    'YB': [
        (from_competition('Swiss Super League'), 'Young Boys'),
        ],
    }




def separate_team(team, data):

    if team not in sep_teams:
        return team
    else:

        candidates = sep_teams[team]
        for c in candidates:
            try:
                pred, nteam = c
            except:
                import pdb; pdb.set_trace()
                continue

            if pred(data):
                return get_team(nteam)

    return get_team(team)


def separate_name(name, magic_d):
    # Confusing.
    # Just pass a predicate function?

    def matching_dicts(src, target):
        for key, value in src.items():
            if target.get(key) != value:
                return False
        return True
    
    #if name == 'Juninho':
    #    import pdb; pdb.set_trace()

    if name not in sep_names:
        return name
    else:
        # Check each option in names.
        # If all the items in the sep_names dict match the items in magic_d, return the new name.
        # Otherwise, proceed.
        names = sep_names[name]
        for n, nd in names:
            if matching_dicts(nd, magic_d):
                return n
    return name
