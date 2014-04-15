#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

from smid.alias import get_team




# Use a partial? memoize?
def from_competition(competition):
    from smid.alias import get_competition

    try:
        c2 = get_competition(competition)
    except:
        import pdb; pdb.set_trace()

    return lambda d: get_competition(d['competition']) == c2


def from_seasons(competition, seasons):
    return lambda d: from_competition(competition)(d) and d['season'] in seasons


sep_names = {

    'Jorge Flores': [
        ('Jorge Villafaña', {'team': 'Chivas USA' }),
        ('Jorge Villafaña', {'team': 'Chivas USA Reserves' }),
        ],

    'Juninho': [
        ('Juninho Paulista', {'team': 'Middlesbrough' }),
        ],

    #'Chris Brown': [
    #    'Chris Brown 1971': {'team': 'FC Dallas' }
    }


sep_teams = {
    'Saint Louis': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Saint Louis University')],
    'Maryland': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Maryland')],
    'West Chester': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'West Chester University')],
    'Connecticut': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Connecticut')],
    'CCNY': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'City College of New York')],
    'Stanford': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Stanford University')],
    'Furman': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Furman University')],
    'Coastal Carolina': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Coastal Carolina University')],
    'Virginia': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Virginia')],
    'UCF': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Central Florida')],
    'San Francisco': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of San Francisco')],
    'Loyola Chicago': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Loyola University Chicago')],
    'West Virginia': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'West Virginia University')],
    'Akron': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Akron')],
    'North Carolina': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'UNC Chapel Hill')],
    'Creighton': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Creighton University')],
    'South Florida': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of South Florida')],
    'New Mexico': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of New Mexico')],
    'Indiana': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Indiana University')],    
    'UMBC': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Maryland Baltimore County')],
    'Michigan': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Michigan')],
    'Tulsa': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Tulsa')],
    'VCU': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Virginia Commonwealth University')],
    'George Mason': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'George Mason University')],
    'Penn': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Pennsylvania')],
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
    'San Diego': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of San Diego')],
    'Lafayette': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Lafayette College')],
    'Air Force': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Air Force Academy')],
    'Washington': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Washington')],
    'Kentucky': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Kentucky')],
    'Syracuse': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Syracuse University')],
    'Cornell': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Cornell University')],
    'Niagara': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Niagara University')],
    'Winthrop': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Winthrop University')],
    'Drexel': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Drexel University')],
    'Northeastern': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Northeastern University')],
    'Georgetown': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Georgetown University')],
    'Marquette': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Marquette University')],
    'Denver': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Denver')],
    'Wisconsin': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Wisconsin')],
    'Quinnipiac': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Quinnipiac University')],
    'Navy': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Naval Academy')],
    'St. Francis (Brooklyn)': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'St. Francis College')],
    'California': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of California, Berkeley')],
    'Fairfield': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Fairfield University')],
    'Charlotte': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'UNC Charlotte')],
    'Providence': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Providence College')],
    'Delaware': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Delaware')],
    'Seattle': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Seattle University')],
    'Milwaukee': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Wisconsin-Milwaukee')],
    'Saint Mary\'s': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'Saint Mary\'s College of California')],
    'Pittsburgh': [(from_competition('NCAA Division I Men\'s Soccer Championship'), 'University of Pittsburgh')],


    'Academica': [
        (from_competition('Primeira Liga'), 'Académica de Coimbra'),
        ],


    'Aguila': [
        (from_competition('Salvadoran Primera División'), 'CD Aguila'),
        (from_competition('CONCACAF Champions League'), 'CD Aguila'),
        (from_competition('Copa Interclubes UNCAF'), 'CD Aguila'),
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
        ],

    'Antigua': [
        (from_competition('Liga Nacional de Guatemala'), 'Antigua GFC')
        ],


    'Arsenal': [
        (from_competition('Argentine Primera División'), 'Arsenal de Sarandi'),
        ],

    #'Atlanta': [
    #    (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
    #    ],

    'Atlético Nacional': [
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        ],

    'Athletic': [
        (from_competition('La Liga'), 'Atletico Madrid'),
        ],

    'Atletico': [
        (from_competition('La Liga'), 'Atletico Madrid'),
        (from_competition('Brasileirão'), 'Atlético Paranaense'),
        ],

    'Barcelona': [
        (from_competition('La Liga'), 'FC Barcelona'),
        (from_competition('UEFA Super Cup'), 'FC Barcelona'),
        (from_competition('FIFA Club World Cup'), 'FC Barcelona'),
        (from_competition('UEFA Champions League'), 'FC Barcelona'),
        (from_competition('Ecuadorian Serie A'), 'Barcelona Sporting Club'),
        (from_competition('Copa Libertadores'), 'Barcelona Sporting Club'),
        ],

    'Berlin': [
        (from_competition('1. Bundesliga'), 'Hertha BSC Berlin'),
        ],


    'Bethlehem': [
        (from_competition('American Soccer League (1921-1933)'), 'Bethlehem Steel'),
        ],


    'Boston': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1928-1929'])), 'Boston Wonder Workers'),
        (from_seasons('American Soccer League (1921-1933)', set(['1929 Fall'])), 'Boston Bears'),
        ],

    'Bohemians': [
        (from_competition('Gambrinus Liga'), 'Bohemians 1905'),
        ],

    'Brooklyn': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1928-1929'])), 'Brooklyn Wanderers'),
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




    'Cartagena': [
        (from_competition('Categoría Primera A'), 'Real Cartagena'),
        ],

    'Central': [
        (from_competition('Uruguayan Primera División'), 'Central Español'),
        ],

    'Chaco': [
        (from_competition('Liga de Fútbol Profesional Boliviano'), 'Chaco Petrolero'),
        ],


    'Chicago': [
        (from_competition('Major League Soccer'), 'Chicago Fire'),
        ],

    'Chicago Fire Reserves': [
        ],

    'Colorado': [
        (from_competition('Major League Soccer'), 'Colorado Rapids'),
        ],


    'Columbus': [
        (from_competition('Major League Soccer'), 'Columbus Crew'),
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
        ],


    'Fall River': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1928-1929', '1930 Spring', '1930 Fall'])), 'Fall River Marksmen'),
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

    'Hakoah': [
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Spring', '1930 Fall'])), 'Hakoah All-Stars'),
        ],

    'Hartford': [
        (from_seasons('American Soccer League (1921-1933)', set(['1927-1928'])), 'Hartford Americans'),
        ],

    'Hamilton': [
        (from_competition('Scottish Premier League'), 'Hamilton Academical'),
        ],

    'Heredia': [
        (from_competition('Liga Nacional de Guatemala'), 'Heredia Jaguares de Peten'),
        (from_competition('Primera División de Costa Rica'), 'CS Herediano'),
        ],

    'Hispano': [
        (from_competition('American Soccer League (1933-1983)'), 'Brooklyn Hispano'),
        (from_competition('Liga Nacional de Honduras'), 'Hispano (Comayagua)'),
        ],

    'Huelva': [
        (from_competition('La Liga'), 'Recreativo Huelva'),
        ],

    'Hungaria': [
        (from_seasons('Eastern Soccer League (1928-1929)', set(['1928-1929 Second Half'])), 'New York Hungaria'),
        #(from_seasons('Eastern Soccer League (1928-1929)', set(['1929 Fall'])), 'Victoria Hungaria'),
        (from_seasons('Eastern Soccer League (1928-1929)', set(['1929 Fall'])), 'New York Hungaria'), # the same, apparently.
        ],

    'Indiana': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926'])), 'Indiana Flooring'),
        ],

    'Irish Americans': [
        (from_competition('American Soccer League (1933-1983)'), 'Kearny Celtic'),
    ],

    'Jersey City': [
        (from_competition('American Soccer League (1921-1933)'), 'Jersey City (ASL)'),

        ],


    'Junior': [
        (from_competition('Categoría Primera A'), 'Junior de Barranquilla'),
        ],

    'Juventud': [
        (from_competition('Liga Nacional de Honduras'), 'Real Juventud'),
        (from_competition('Uruguayan Primera División'), 'Juventud de Las Piedras'),
        ],

    'Liverpool': [
        (from_competition('Uruguayan Primera División'), 'Liverpool (Montevideo)'),
        ],

    'Lokomotiv': [
        (from_competition('Russian Premier League'), 'Lokomotiv Moscow'),
        ],

    'Los Andes': [
        (from_competition('Argentine Primera División'), 'Los Andes de Lomas de Zamora'),
        ],

    'Marte': [
        (from_competition('Salvadoran Primera División'), 'C.D. Atlético Marte'),
        ],

    'Nacional': [
        (from_competition('Paraguayan Primera División'), 'Club Nacional'),
        (from_competition('Categoría Primera A'), 'Atlético Nacional'),
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        ],

    'Necaxa': [
        (from_competition('Liga Nacional de Honduras'), 'CD Necaxa'),
        ],

    'Newark': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1930 Spring'])), 'Newark Skeeters'),
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Fall',])), 'Newark Americans'),
        ],

    'New Bedford': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1925-1926', '1929 Fall', '1930 Spring', '1930 Fall'])), 'New Bedford Whalers'),
        ],

    'New York': [
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Fall'])), 'New York SC Giants'),
        ],

    'New York Giants': [
        (from_competition('Eastern Soccer League (1928-1929)'), 'New York SC Giants'),
        (from_seasons('American Soccer League (1921-1933)', set(['1923-1924', '1924-1925', '1925-1926', '1926-1927', '1927-1928', '1928-1929', '1930 Spring'])), 'New York SC Giants'),

        (from_competition('American Soccer League (1921-1933) Playoffs'), 'New York National Giants'),
        (from_seasons('American Soccer League (1921-1933)', set(['1930 Fall', '1931 Spring', '1931 Fall', '1932 Spring', '1932 Fall'])), 'New York National Giants'),
        ],


    'New York Hakoah': [
        (from_competition('American Soccer League (1933-1983)'), 'Hakoah (ASL2)'),
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

    'Paris': [
        (from_competition('Ligue 1'), 'Paris Saint-Germain'),
        ],


    'Pawtucket': [
        (from_seasons('American Soccer League (1921-1933)', set(['1925-1926', '1929 Fall', '1930 Spring', '1930 Fall'])), 'Pawtucket Rangers'),
        ],


    'Philadelphia': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1929 Fall'])), 'Philadelphia Field Club'),
        ],


    'Providence': [
        (from_seasons('American Soccer League (1921-1933)', set(['1924-1925', '1928-1929', '1929 Fall', '1930 Spring', '1930 Fall'])), 'Providence Clamdiggers'),
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


    'River Plate': [
        (from_competition('Uruguayan Primera División'), 'River Plate (Montevideo)'),
        ],

    'River': [
        (from_competition('Uruguayan Primera División'), 'River Plate (Montevideo)'),
        ],


    'Sacachispas': [
        (from_competition('Liga Nacional de Guatemala'), 'CSD Sacachispas')
        ],

    'Salzburg': [
        (from_competition('Liga Nacional de Honduras'), 'Honduras Salzburg'),
        ],

    'San Jose': [
        (from_competition('Liga de Fútbol Profesional Boliviano'), 'CD San José',),
        ],

    'Santa Fe': [
        (from_competition('Categoría Primera A'), 'Independiente Santa Fe'),
        ],

    'Santa Lucia': [
        (from_competition('Liga Nacional de Guatemala'), 'Santa Lucía Cotzumalguapa'),
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
        ],


    'Slavia': [
        (from_competition('Gambrinus Liga'), 'Slavia Prague'),
        (from_competition('UEFA Champions League'), 'Slavia Prague'),
        ],

    'Sociedad': [
        (from_competition('La Liga'), 'Real Sociedad'),
        ],

    'Sparta': [
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


    'Standard': [
        (from_competition('Belgian Pro League'), 'Standard Liège'),
        ],

    'Sturm': [
        (from_competition('Austrian Bundesliga'), 'Sturm Graz'),
        ],


    'Talleres': [
        (from_competition('Copa Libertadores'), 'Talleres de Córdoba',),
        ],



    'UCD': [
        (from_competition('League of Ireland'), 'University College Dublin'),
        ],

    'Universidad': [
        (from_competition('Liga Nacional de Honduras'), 'Pumas UNAH'),
        ],

    'Universidad Católica': [
        (from_competition('Ecuadorian Serie A'), 'Universidad Católica del Ecuador'),
        ],

    'Union': [
        (from_competition('Argentine Primera División'), 'Unión de Santa Fe'),
        ],

    'Valencia': [
        (from_competition('Liga Nacional de Honduras'), 'Municipal Valencia'),
        (from_competition('La Liga'), 'Valencia CF'),
        (from_competition('UEFA Super Cup'), 'Valencia CF'),

        ],

    'Victoria': [
        (from_competition('Liga Nacional de Honduras'), 'CD Victoria'),
        ],


    'Viking': [
        (from_competition('Tippeligaen'), 'Viking FK'),
        ],

    'Vitoria': [
        (from_competition('Brasileirão'), 'EC Vitória'),
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
        for pred, nteam in candidates:
            if pred(data):
                return get_team(nteam)

    return get_team(team)


def separate_name(name, magic_d):
    # Confusing.
    # Just pass a predicate function?

    if name not in sep_names:
        return name
    else:
        names = sep_names[name]
        for n, nd in names:
            for k, v in nd.items():
                if magic_d.get(k) != v:
                    return name
            #import pdb; pdb.set_trace()
            #x = 5
            return n
    return name
