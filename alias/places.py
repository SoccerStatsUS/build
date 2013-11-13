#!/usr/local/bin/env python
# -*- coding: utf-8 -*-


def get_place(s):
    """
    Recursive. 
    """

    s = s.strip()
    if s in places:
        return get_place(places[s])
    else:
        return s


places = {
    'Cricket Ground, Sydney': 'Sydney Cricket Ground',
    'Sports Ground, Sydney': 'Sydney Sports Ground',
    'Estadio Municipal, Concepcion': 'Estadio Municipal de Concepción',
    'Estadio Regional, Antofagasta': 'Estadio Regional de Antofagasta',
    'National Soccer Stadium, Toronto': 'BMO Field',
    'Olympic Stadium, Montreal': 'Montreal Olympic Stadium',
    'Ataturk Stadium, Bursa': 'Bursa Ataturk Stadium',
    'Stedelijk Olympisch, Antwerp': 'Stedelijk Olympisch Stadion',
    'Idrottsplats, Råsunda': 'Råsunda Idrottsplats',
    'Idrottsplats Traneberg': 'Traneberg Idrottsplats',
    'Sportplats, Traneberg': 'Traneberg Sportplats',
    'Olympic, Stockholm': 'Olympic Stadion, Stockholm',
    'Bosuil, Antwerp': 'Bosuilstadion',
    'De Bosuil, Antwerp': 'Bosuilstadion',

    # Generic
    'Away': 'away',
    'Neutral': 'neutral',
    'Home': 'home',

    # Countries
    'Trinidad': 'Trinidad and Tobago',
    'USA': 'United States',
    'holland': 'Netherlands',
    'Holland': 'Netherlands',
    'St. Lucia': 'Saint Lucia',

    'Exhibition Stadium, Toronto': 'CNE Stadium',


    # England
    'Griffin Park (Brentford), London': 'Griffin Park',
    'Griffin Park Brentford, London': 'Griffin Park',

    # Uruguay
    'Central Park Stadium, Montevideo, Uruguay': 'Parque Central',

    # Peru
    'Estadio Nacional, Lima': 'Estadio Nacional de Peru',
    'Estadio Monumental, Lima': 'Estadio Monumental "U"',

    'Agawam HS': 'Agawam High School',
    'Agawam H.S.': 'Agawam High School',
    'Randalls Island': 'Randall\'s Island, New York',
    'Randall\'s Island': 'Randall\'s Island, New York',


    'David\'s Stadium, Newark, NJ': 'Ruppert Stadium, Newark, NJ',
    'Davids Stadium, Newark, NJ':' Ruppert Stadium, Newark, NJ',

    'Memorial Coliseum, Los Angeles': 'Los Angeles Memorial Coliseum',

    'KSU Soccer Stadium, Kennesaw, GA': 'Kennesaw State University Stadium',
    'FAU Soccer Field, Boca Raton, FL': 'FAU Soccer Stadium',
    'Memorial Stadium, Everett, MA': 'Everett Memorial Stadium',
    'Memorial Stadium, Portland, ME': 'Memorial Stadium (Maine)',

    # Spain
    'Nuevo Estadio, Elche': 'Estadio Manuel Martínez Valero',

    # Japan
    'Universiad Memorial Stadium, Kobe, Japan': 'Kobe Universiade Memorial Stadium',
    'Olympic Stadium, Tokyo': 'Tokyo National Olympic Stadium',
    'National Stadium, Tokyo, Japan': 'Tokyo National Olympic Stadium',

    # Mexico

    'Estadio Universitario, Monterrey': 'Estadio Universitario de Monterrey',
    'Estadio Olimpico, Villahermosa, México': 'Estadio Olimpico (Tabasco)',
    'Estadio Nou Camp, Leon, Guanajuato': 'Estadio León',
    'Stadium Universitario, Monterrey, Mexico': 'El Volcan',
    'Estadio Universitario, San Nicolas': 'El Volcan',
    'Estadio Universitario, San Nicolas de los Garza': 'El Volcan',

    # Italy
    'Stadio Municipal, L\'Aquíla': 'Stadio Tommaso Fattori',
    'Stadio Municipal, L\'Aquila': 'Stadio Tommaso Fattori',

    # Brazil
    'Estadio Olimpico Monumental (Porto Alegre)': 'Estádio Olímpico Monumental',
    'Estadio Olimpico Monumental, Porto Alegre': 'Estádio Olímpico Monumental',
    'Estadio Olimpico (Porto Alegre)': 'Estádio Olímpico Monumental',
    'Estadio Olimpico, Porto Alegre': 'Estádio Olímpico Monumental',
    'Estadio Independencia, Belo Horizonte, Brazil': 'Estádio Independência',

    # Netherlands
    'Enschede Stadium, Enschede': 'De Grolsch Veste',

    # Russia
    'Dinamo Stadium, Moscow': 'Moscow Dinamo Stadium',

    # Belarus
    'Dinamo Stadium, Minsk': 'Dynama Stadium',

    # Costa Rica
    'Estadio Nacional, San Jose, Costa Rica': 'Estadio Nacional de Costa Rica',

    # Nicaragua
    'Estadio Independencia, Esteli': 'Estadio Independencia (Esteli)',


    # Trinidad
    'Centre of Excellence, Port of Spain, Trinidad and Tobago': 'Dr. João Havelange Centre of Excellence',

    # Argentina
    'Estadio Monumental, Buenos Aires': 'Estadio Monumental Antonio Vespucio Liberti',

    # Lima
    'Estadio Miguel Grau, Piura, Peru': 'Estadio Miguel Grau (Piura)',

    # Argentina
    'Estadio del Bicentenario, San Juan, Argentina': 'Estadio San Juan del Bicentenario',


    'Stade Dillon, Fort-de-France, Martinique': 'Stade Pierre-Aliker',
    'Estadio Pueblo Nuevo, San Cristobal, Venezuela': 'Estadio Polideportivo de Pueblo Nuevo',
    'Toyota Arena, Prague, Czech Republic': 'Generali Arena',
    'National Stadium, Kingston, Jamaica': 'Independence Park (Jamaica)',
    'National Stadium, Kingston': 'Independence Park (Jamaica)',
    'Greenfield Stadium, Trelawny, Jamaica': 'Greenfield Stadium (Trelawny)',
    'Independence Park, Kingston, Jamaica': 'Independence Park (Jamaica)',
    'Estadio Monumental, Guayaquil, Ecuador': 'Estadio Monumental Isidro Romero Carbo',
    'Estadio Campus Municipal, Maldonado, Uruguay':    'Estadio Suppici',

    'Estadio Olimpico, Caracas, Venezuela': 'Estadio Olímpico de la UCV',
    'Estadio Olimpico, Caracas': 'Estadio Olímpico de la UCV',

    'Independiente Stadium, Avellaneda, Argentina': 'Estadio de Independiente',
    'Estadio Centenario, Armenia, Colombia': 'Estadio Centenario de Armenia',
    'Estadio Centenario, Armenia': 'Estadio Centenario de Armenia',
    'Estadio Monumental, Buenos Aires, Argentina': 'Estadio Monumental Antonio Vespucio Liberti',
    'Estadio Nacional, Santiago, Chile': 'Estadio Nacional Julio Martínez Prádanos',
    'Estadio Nacional, Lima, Peru': 'Estadio Nacional de Peru',
    'FIFA World Cup Stadium, Hamburg': 'HSH Nordbank Arena',
    'FIFA World Cup Stadium, Dortmund': 'Signal Iduna Park',
    'FIFA World Cup Stadium, Frankfurt, Frankfurt/Main': 'Commerzbank-Arena',
    'FIFA World Cup Stadium, Cologne': 'RheinEnergieStadion',
    'FIFA World Cup Stadium, Hanover': 'AWD-Arena',
    'Stade Municipal, Toulouse': 'Stade Municipal de Toulouse',
    'San Paolo, Naples': 'Stadio San Paolo',
    'Estadio Nacional, Santiago': 'Estadio Nacional Julio Martínez Prádanos',

    'Olympic Park, Melbourne, Australia': 'Olympic Park Stadium',

    'Randall\'s Island, NYC': 'Downing Stadium',
    'Stade Olympique, Colombes, Paris': 'Stade Olympique Colombes',
    'Republican Stadium, Kiev': 'Kiev Olympic Stadium',
    'Lenin Stadium, Moscow': 'Luzhniki Stadium',
    'FIFA World Cup Stadium, Gelsenkirchen': 'Veltins-Arena', 
    'Estadío Tropical, Havana, Cuba': 'Estadio Pedro Marrero',
    'Tropical Stadium, Havana, Cuba': 'Estadio Pedro Marrero',
    'Estadío Olimpico, Mexico City': 'Estadio Olímpico Universitario',
    'Estadío Olimpica, Ciudad de México': 'Estadio Olímpico Universitario',
    'Baseball Stadium, Baltimore': 'Memorial Stadium Baltimore',
    'Estadío Universitario, Monterrey': 'Estadío Universitario de Monterrey',
    'Estadío Nacional, Tegucigalpa': 'Estadio Tiburcio Carías Andino',
    'Estadio Nacional, Tegucigalpa': 'Estadio Tiburcio Carías Andino',
    'Veteran\'s Stadium, New Britain, CT': 'New Britain Veterans Stadium',
    'Memorial Stadium, Seattle': 'Seattle High School Memorial Stadium',
    'Edinburg Field': 'Edinburg Stadium',
    'Empire Field Stadium': 'Empire Field',
    'JC Handly Park': 'JC Handley Park',
    'Celtic Park, Long Island, NY': 'Celtic Park, Queens, NY',
    'Cricket Club Grounds, Livingston, Staten Island, NY': 'Staten Island Cricket Grounds',
    'National Stadium (Olympic Stadium), Tokyo': 'National Olympic Stadium, Tokyo',
    'Maracanã - Estádio Jornalista Mário Filho, Rio De Janeiro': 'Estádio do Maracanã',
    'Pacaembu - Estádio Municipal Paulo Machado de Carv, Sao Paulo': 'Estádio do Pacaembu',
    'Morumbi - Estádio Cícero Pompeu de Toledo, Sao Paulo': 'Estádio do Morumbi',
    'Independencia, Belo Horizonte': 'Estádio Independência, Belo Horizonte',
    'Velodrome, Marseilles': 'Stade Vélodrome, Marseilles',
    'Olimpico, Rome': 'Stadio Olimpico, Rome, Italy',
    'Delle Alpi, Turin': 'Stadio delle Alpi',
    'Hillsborough, Sheffield': 'Hillsborough Stadium, Sheffield',

    'Compton Ave Park': 'Compton Avenue Park',
    'Capitoline Lake': 'Capitoline Grounds',
    'Cal State Fullerton': 'Titan Stadium, Fullerton, CA',
    'Richmond City Stadium': 'City Stadium, Richmond, VA',

    'Memorial Stadium Los Angeles': 'Los Angeles Memorial Coliseum',
    'Memorial Stadium, Long Beach, CA': 'Veterans Memorial Stadium, Long Beach, CA',

    'St. George Cricket Grounds, Hoboken': 'St. George\'s Cricket Grounds, Hoboken',

    'Southwestern College, San Diego, California': 'Southwestern College, Chula Vista, California',
    'Molson Stadium, Montreal': 'Percival Molson Memorial Stadium',
    'Olympic Park, Paterson': 'Olympic Field, Paterson',
    'Olympic Park, Paterson, NJ': 'Olympic Field, Paterson',
    'Island Stadium, Toronto': 'Hanlan\'s Point Stadium',

    'SAS Stadium, Cary, NC': 'WakeMed Soccer Park',
    'SAS Soccer Park, Cary, NC': 'WakeMed Soccer Park',

    'Dudley Stadium, El Paso, TX': 'Dudley Field',
    'Douglas Stadium, San Diego, CA': 'Merrill Douglas Stadium',
    'Santa Ana Bowl, Santa Ana, CA': 'Santa Ana Stadium',

    'Memorial Stadium, Seattle, WA': 'Memorial Stadium (Seattle), Seattle, WA',

    'Clark\'s Field, East Newark, NJ': 'Clark Field, Newark, NJ',
    'Clark\'s Field, Newark, NJ': 'Clark Field, Newark, NJ',

    'National Sports Center, Blaine, MN': 'National Sports Center Stadium',
    
}


states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'FL': 'Florida',
    'HI': 'Hawaii',
    'GA': 'Georgia',
    'IA': 'Iowa',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'ON': 'Ontario',
    'OR': 'Oregon',
    'OK': 'Oklahoma',
    'PA': 'Pennsylvania',
    'QC': 'Quebec',
    'OH': 'Ohio',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tenneessee',
    'TX': 'Texas',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming',
    }
