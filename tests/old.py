import unittest

# A result without a date should definitely raise an error.
# Is it better to store goal minute as a string (for, e.g. 45+2) or as an integer (for sorting...)
# Might be a good idea to define, e.g. if month >= 7, it's 2010, otherwise, 2011.
# Need to review 


# Split up single-line tests and multi-line tests.
# Distinguish results from scraping lines, scraping whole text.
# Possibly...Scrape single lines first, yielding a list of dicts, then
# interpret those dicts. (reduce)


# Do goals need game identifiers?
# They should probably just be included in the fucking game dict.

YEAR = 2011
COMPETITION = "TEST COMPETITION"

class TestScraperCache(unittest.TestCase):
    # The scraper saves whole html files, which can be encoded as pretty much anything.
    # This is just to make sure that everything is getting saved correctly.
    # Whatever the encoding.
    
    def test_normal():
        pass


    def test_european():
        pass


    def test_whatever():
        pass



# All below  are all RSSSF tests...
class TestLines(unittest.TestCase):
    
    def test_ignore_standings():
        l = [
            '1.Estudiantes (La Plata)                19  14  3  2  32- 8  45  Champions',
            ' 1.FC Juventus         38 26  8  4  67-27  86  Stripped of Title July 2006',
            '1.Triestina         3   3  0  0   6- 2   9  Qualified '
            ]

        for e in l:
            assertEqual(None, SCRAPE(e))
                        
                        

    def test_ignore_miscellaneous():
        l = [
            'NB: Philadelphia Union were added for 2010',
            'Bologna relegated',
            ]
        for e in l:
            assertEqual(None, SCRAPE(e))


    def test_normal_score():
        # Please note this is a different Arsenal!
        s = 'Arsenal                 1-2 Lanús                   '
        r = {
            'type': 'result',
            'date': None
            'home_team': 'Arsenal',
            'away_team': 'Lanús',
            'home_score': 1,
            'away_score': 2,
            'notes': '',
            }
        assertEqual(SCRAPE(s), r)
        
    def test_with_comment():
        s = 'Estudiantes             2-0 Quilmes                 [at Quilmes]'
        r = {
            'type': 'result',
            'date': None
            'home_team': 'Estudiantes'
            'away_team': 'Quilmes',
            'home_score': 2,
            'away_score': 0,
            'notes': 'at Quilmes',
            }
        assertEqual(SCRAPE(s), r)

    def test_score_plus_date():
        # Need to test date progression at New Year's
        s = 'Salernitana 2-1 Palermo                [Sep 28]'
        r = {
            'type': 'result',
            'date': datetime.datetime(YEAR, 9, 28),
            'home_team': 'Salernitana',
            'away_team': 'Palermo',
            'home_score': 2,
            'away_score': 1,
            'notes': '',
            }
        assertEqual(SCRAPE(s), r)

    def test_competition_plus_date():
        # Do an integration test after this to make sure that it works well with two lines.
        s = 'Semifinals [May 11]'
        r = [
            {
                'type': 'competition',
                'name': 'Semifinals',
                },
            {
                'type': 'date',
                'date': datetime.datetime(YEAR, 5, 11),
                },
            ]
        assertEqual(SCRAPE(s), r)
                

    def test_multi_date():
        # Do an integration test after this to make sure that it works well with two lines.
        s = 'Semifinals [May 11 and 18]'
        r = [
            {
                'type': 'competition',
                'name': 'Semifinals',
                },
            {
                'type': 'date',
                'date': datetime.datetime(year, 5, 11),
                },

            {
                'type': 'date',
                'date': datetime.datetime(year, 5, 18),
                },
            ]
        assertEqual(SCRAPE(s), r)

    def test_multi_score():
        s = 'Cagliari    1-1 1-3 Inter'
        r = [
            {
                'type': 'result',
                'date': None,
                'home_team': 'Cagliari'
                'away_team': 'Inter',
                'home_score': 1,
                'away_score': 1,
                'notes': '',
                },
            {
                'type': 'result',
                'date': None,
                'home_team': 'Inter',
                'away_team': 'Cagliari',
                'home_score': 3,
                'away_score': 1,
                'notes': '',
                },
            ]


    def test_multi_score_with_date():
        # This is not a fair test. Need another date at the top.
        # DEAR JESUS
        
        # Probably ought to do a variety of these.
        # 1st leg, First Leg, 2nd Leg, 2nd leg, etc.
        'Cagliari    1-1 1-3 Inter                  [1st leg May 12]'
        r = [
            {
                'type': 'result',
                'date': None,
                'home_team': 'Cagliari'
                'away_team': 'Inter',
                'home_score': 1,
                'away_score': 1,
                'notes': '',
                },
            {
                'type': 'result',
                'date': datetime.datetime(YEAR, 5, 12),
                'home_team': 'Inter',
                'away_team': 'Cagliari',
                'home_score': 3,
                'away_score': 1,
                'notes': '',
                },
            ]


    def test_competitions():
        # Sort of testing competition names.
        # Sort of testing spaces.
        # Is there any point in recording rounds?
        # Maybe better just to return a blank competition.
        l = [
            'Round 15 ',
            ' Conference Semifinals',
            'Conference Finals ',
            ]

        r = [
            {
                'type': 'competition',
                'name': 'Round 15'
                },
            {
                'type': 'competition',
                'name': 'Conference Semifinals',
                },
            {
                'type': 'competition',
                'name': 'Conference Finals',
                },
            ]

    def test_parse_final():
        # Don't think I want to try to parse locations...pretty much impossible?
        # Need a multi-line test here.
        s = 'Final [Nov 21, MBO Field, Toronto]'
        r = [
            {
                'type': 'competition',
                'name': 'Final',
                },
            {
                'type': 'date'
                'date': datetime.datetime(YEAR, 11, 21)
                },
            ]

    def test_parse_final():
        # Don't think I want to try to parse locations...pretty much impossible?
        # Need a multi-line test here.
        s = 'Final [Nov 21, MBO Field, Toronto]'

        r = [
            {
                'type': 'competition',
                'name': 'Final',
                },
            {
                'type': 'date'
                'date': datetime.datetime(YEAR, 11, 21)
                },
            ]

    def test_final_integration():
        s = """[Final [Nov 21, MBO Field, Toronto]'
               Colorado Rapids        2-1 FC Dallas              [aet]
               [Casey 57, John 107og; Ferreira 35]
            """

        r = {
            'type': 'result',
            'date': datetime.datetime(YEAR, 11, 21)
            'home_team': 'Colorado Rapids'
            'away_team': 'FC Dallas'
            'home_score': 2,
            'away_score': 1,
            'notes': '',
            }

        goals = [
            {
                'type': 'goal',
                'player': 'Casey',
                'minute': 57,
                },
            {
                'type': 'goal',
                'player': 'Ferreira',
                'minute': 35,
                },
            {
                'type': 'goal',
                'player': 'John',
                'minute': 107,
                'type': 'own goal',
                },
            ]


    def test_goals():

        s = '[Andrea Caracciolo 39; Gianfranco Zola 13pen, Antonio Langella 82]'
        r = [
            {
                'type': 'goal'
                'player': 'Andrea Caracciolo',
                'minute': 39,
                },
            {
                'type': 'goal'
                'player': 'Gianfranco Zola' 
                'minute': 13,
                'type': 'penalty',
                },
            {
                'type': 'goal'
                'player': 'Antonio Langella'
                'minute': 82,
                }
            ]
        
    def test_multi_goals():
                
        s = '  [Adriano 30, 35]'
        r = [
                {
                    'type': 'goal'
                    'player': 'Adriano', 
                    'minute': 30,
                    },
                {
                    'type': 'goal'
                    'player': 'Adriano', 
                    'minute': 35,
                    },
                ]
        assertEqual(r, SCRAPE(s))



    def test_goals_multiline():
        s = """  [Vincenzo Montella 9, Francesco Totti 57, Daniele De Rossi 74; 
   Esteban Cambiasso 45+1, Juan Sebastian Veron 51, Alvaro Recoba 54]"""
        r = [
            {
                'type': 'goal'
                'player': 'Vicenzo Montella'
                'minute': 9,
                },
            {
                'type': 'goal'
                'player': 'Francesco Totti',
                'minute': 57,
                },
            {
                'type': 'goal'
                'player': 'Daniele De Rossi',
                'minute': 74,
                },
            {
                'type': 'goal',
                'player': 'Esteban Cambiasso'
                'minute': 45,
                },
            {
                'type': 'goal',
                'player': 'Juan Sebastian Veron 51',
                'minute': 51,
                },
            {
                'type': 'goal',
                'player': ', Alvaro Recoba'
                'minute': 54,
                },
            ]
            assertEqual(r, SCRAPE(s))



class TestGameDetail():
    # Oh great what am I thinking?
    
    def test_detail():
        """
        First Leg [Jun 12, Stadio Olimpico, Roma]
Roma: Gianluca Curci; Christian Panucci, Matteo Ferrari, Cristian Chivu,
      Leandro Cufré (Giuseppe Scurto 82); Valerio Virga (Vincenzo Montella 58),
      Olivier Dacourt, Simone Perrotta; Francesco Totti; Alessandro Mancini
      (Greco 72), Antonio Cassano; coach: Bruno Conti;
Inter: Francesco Toldo; Javier Zanetti, Marco Materazzi, Sinisa Mihajlovic,
       Giuseppe Favalli; Dejan Stankovic, Esteban Cambiasso, Zé María, Kily
       Gonzalez (Andy Van der Meyde 86); Leite Ribeiro Adriano, Obafemi Martins 
       (Julio Cruz 76); coach: Roberto Mancini;
Ref: PierLuigi Collina  
Yellow Cards: Matteo Ferrari 29, Cristian Chivu, Simone Perrotta 73. 
Att: 73,437
       """


class TestChampionsLeague():

    def test_champs_qualifying():
        s = 'Makedonija Skopje        Mac  BATE Barysau             Bls   0-2  0-2  0-4x"'
        r = [
            {
                'type': 'result',
                'date': None,
                'home_team': 'Makedonija Skopje',
                'away_team': 'BATE Barysau',
                'home_score': 0,
                'away_score': 2,
                'notes': '',
                },
            {
                'type': 'result',
                'date': None,
                'home_team': 'BATE Barysau',
                'away_team': 'Makedonija Skopje',
                'home_score': 2,
                'away_score': 0,
                'notes': '',
                },
            ]



    def test_cl_integration():
        # Oh great idea assholes.
        # How to test this?
        # Feed the whole thing to a parser, and make sure that we get the correct results back.
        # Um...need to do something about that penalties part at the end?....
        """
        Preliminary Round (Jul 1 and 8)
Hibernians               Mlt  Mogren Budva             Mng   0-2  0-4  0-6x
Tre Fiori                SMa  UE Sant Julià            And   1-1  1-1  2-2y 4-5p
x 1st leg Jun 30, 2nd leg in Podgorica
y 2nd leg Jul 7
        """
        r = [
        {
            'date': datetime.datetime(YEAR, 6, 30)
            'type': 'result',
            'home_team': 'Hibernians',
            'away_team': 'Mogren Budva',
            'home_score': 0,
            'away_score': 2,
            'notes': '',
            }

        {
            'date': datetime.datetime(YEAR, 7, 8)
            'type': 'result',
            'away_team': 'Hibernians',
            'home_team': 'Mogren Budva',
            'away_score': 0,
            'home_score': 4,
            'notes': '',
            },
        {
            'date': datetime.datetime(YEAR, 7, 1)
            'type': 'result',
            'home_team': 'Tre Fiori'
            'away_team': 'UE Sant Julià',
            'home_score': 1,
            'away_score': 1,
            'notes': '',
            }

        {
            'date': datetime.datetime(YEAR, 7, 7)
            'type': 'result',
            'home_team': 'UE Sant Julià',
            'away_team': 'Tre Fiori'
            'home_score': 1,
            'away_score': 1,
            'notes': '',
            }
        ]
        

    def test_weird_score():
        # parentheses represent halftime goals. Who the fuck cares?
        s = 'Sep 15: Maccabi Haifa            (0) 0 Bayern München           (0) 3x'
        r = {
            'date': datetime.datetime(2010, 9,15),
            'home_team': 'Maccabi Haifa',
            'away_team': 'Bayern München',
            'home_score': 0,
            'away_score': 3,
            'reference': 'x',
            'notes': '',
            }


    def test_scores():
        s = """
           Second Qualifying Phase (Jul 16 and 23)'
           Falkirk                  Sco  FC Vaduz                 Lie   1-0  0-2  1-2  aet
        """
        r = [
            {
                'date': datetime.datetime(YEAR, 7, 16),
                'home_team': 'Falkirk',
                'away_team': 'FC Vaduz',
                'home_score': 1,
                'away_score': 0,
                'notes': '',
                },
            {
                'date': datetime.datetime(YEAR, 7, 23)
                'home_team': 'FC Vaduz'
                'away_team': 'Falkirk',
                'home_score': 2,
                'away_score': 0,
                'notes': '',
                },
            ]
        
