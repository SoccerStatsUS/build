from smid.alias import get_team

magic_names = {

    'Jorge Flores': [
        ('Jorge Villafaña', {'team': 'Chivas USA' }),
        ('Jorge Villafaña', {'team': 'Chivas USA Reserves' }),
        ],


    #'Chris Brown': [
    #    'Chris Brown 1971': {'team': 'FC Dallas' }
    }


# Use a partial?
def from_competition(competition):
    return lambda d: d['competition'] == competition

magic_teams = {

    'Aguila': [
        (from_competition('Salvadoran Primera División'), 'CD Aguila'),
        (from_competition('Copa Interclubes UNCAF'), 'CD Aguila'),
        ],

    'Alianza': [
        (from_competition('Salvadoran Primera División'), 'Alianza F.C.'),
        (from_competition('Copa Interclubes UNCAF'), 'Alianza F.C.'),
        ],

    'America': [
        (from_competition('Liga MX'), 'Club America'),
        (from_competition('Liga MX Liguilla'), 'Club America'),
        (from_competition('Categoría Primera A'), 'America de Cali')
        ],

    'Antigua': [
        (from_competition('Liga Nacional de Guatemala'), 'Antigua GFC')
        ],


    'Arsenal': [
        (from_competition('Argentine Primera División'), 'Arsenal de Sarandi'),
        ],

    'Atlético Nacional': [
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        ],

    'Cartagena': [
        (from_competition('Categoría Primera A'), 'Real Cartagena'),
        ],

    'Central': [
        (from_competition('Uruguayan Primera División'), 'Central Español'),
        ],

    'Estudiantes': [
        (from_competition('Liga MX'), 'Tecos'),
        (from_competition('Copa Libertadores'), 'Estudiantes de La Plata'),
        (from_competition('Argentine Primera División'), 'Estudiantes de La Plata'),
        ],

    'Heredia': [
        (from_competition('Liga Nacional de Guatemala'), 'Heredia Jaguares de Peten'),
        (from_competition('Primera División de Costa Rica'), 'CS Herediano'),
        ],

    'Junior': [
        (from_competition('Categoría Primera A'), 'Junior de Barranquilla'),
        ],

    'Juventud': [
        (from_competition('Liga Nacional de Honduras'), 'Real Juventud'),
        ],

    'Liverpool': [
        (from_competition('Uruguayan Primera División'), 'Liverpool (Montevideo)'),
        ],

    'Los Andes': [
        (from_competition('Argentine Primera División'), 'Los Andes de Lomas de Zamora'),
        ],

    'Marte': [
        (from_competition('Salvadoran Primera División'), 'C.D. Atlético Marte'),
        ],

    'Nacional': [
        (from_competition('Categoría Primera A'), 'Atlético Nacional'),
        (from_competition('Liga Panameña de Fútbol'), 'Atlético Nacional (Panama)'),
        ],

    'Necaxa': [
        (from_competition('Liga Nacional de Honduras'), 'CD Necaxa'),
        ],

    'Olimpia': [
        (from_competition('Liga Nacional de Honduras'), 'CD Olimpia'),
        (from_competition('CONCACAF Champions League'), 'CD Olimpia'),
        (from_competition('Copa Interclubes UNCAF'), 'CD Olimpia'),
        (from_competition('Copa Mercosur'), 'Club Olimpia'),
        (from_competition('Copa Libertadores'), 'Club Olimpia'),
        (from_competition('Uruguayan Primera División'), 'Olimpia (Uruguay)'),
        ],

    'Real Espana': [
        (from_competition('Liga Nacional de Honduras'), 'Real C.D. España'),
        ],

    'Racing': [
        (from_competition('Liguilla Pre-Libertadores de América (Uruguay)'), 'Racing Club de Montevideo'),
        (from_competition('Uruguayan Primera División'), 'Racing Club de Montevideo'),
        (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
        ],

    'Racing Club': [
        (from_competition('Liguilla Pre-Libertadores de América (Uruguay)'), 'Racing Club de Montevideo'),
        (from_competition('Uruguayan Primera División'), 'Racing Club de Montevideo'),
        (from_competition('Argentine Primera División'), 'Racing Club de Avellaneda'),
        ],

    'River Plate': [
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

    'Santa Lucia': [
        (from_competition('Liga Nacional de Guatemala'), 'Santa Lucía Cotzumalguapa'),
        ],

    'Santos': [
        (from_competition('Liga MX'), 'Santos Laguna'),
        (from_competition('Liga MX Liguilla'), 'Santos Laguna'),
        (from_competition('Primera División de Costa Rica'), 'Santos de Guápiles'),
        ],

    'Sport': [
        (from_competition('Copa Libertadores'), 'SC Recife'),
        ],

    'Sporting': [
        (from_competition('Liga Panameña de Fútbol'), 'Sporting San Miguelito'),
        ],

    'Universidad': [
        (from_competition('Liga Nacional de Honduras'), 'Pumas UNAH'),
        ],

    'Union': [
        (from_competition('Argentine Primera División'), 'Unión de Santa Fe'),
        ],

    'Valencia': [
        (from_competition('Liga Nacional de Honduras'), 'Municipal Valencia'),
        ],

    'Victoria': [
        (from_competition('Liga Nacional de Honduras'), 'CD Victoria'),
        ],

    'Wanderers': [
        (from_competition('Uruguayan Primera División'), 'Montevideo Wanderers'),
        ],
    }


def get_magic_team(team, data):

    #if team == 'America':
    #    import pdb; pdb.set_trace()


    if team not in magic_teams:
        return team
    else:
        candidates = magic_teams[team]
        for pred, nteam in candidates:
            if pred(data):
                return get_team(nteam)

    return get_team(team)


def get_magic_name(name, magic_d):
    # Confusing.
    # Just pass a predicate function?

    if name not in magic_names:
        return name
    else:
        names = magic_names[name]
        for n, nd in names:
            for k, v in nd.items():
                if magic_d.get(k) != v:
                    return name
            #import pdb; pdb.set_trace()
            #x = 5
            return n
    return name
