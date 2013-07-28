# Need to set up a lot of tests to validate scraped data.

# Also need to set up a framework to throw corpuses against each
# other and make sure they are the same.

#import unittest

# Looks like these should probably be merged with the other scrapers eventually...

# Proobably should grop tests by type.
"""
class TestMLSScraper(unittest.TestCase):


    def test_cnnsi_mls_score(): 
        url = 'http://sports.sportsillustrated.cnn.com/mls/scoreboard_daily.asp?gameday=20110817'
        games = scrape_games(url)
        
        # Should I parse date from url?
        # Should I parse goals out of here?
        first_game = {
            'date':'',
            'location': '',
            'home_team': 'New England',
            'away_team': 'Houston',
            'home_score': '1',
            'away_score': '1',
            'competition': '',
            'round': '',
            'notes': '',
            'source': url,
            }

        second_game = {
            'date':'',
            'location': '',
            'home_team': 'Sporting Kansas City',
            'away_team': 'Portland',
            'home_score': '3',
            'away_score': '1',
            'competition': '',
            'round': '',
            'notes': '',
            'source': url,
            }

    def test_mls_concacaf_score():
        """
        
        """
        url = "http://www.mlssoccer.com/ccl/schedule2011"
        games = scrape_games(url)

        first_game = {
            "date": "Aug. 16\n8 pm",
            "location": "Estadio Corona",
            "home_team": "Santos Laguna (MEX)",
            "away_team": "Real España (HON)",
            "home_score": "3",
            "away_score": "2",
            "competition": "CONCACAF Champions League",
            "round": "Group Stage",
            "notes": "",
            "source": url,
            }

        
        
        another_game = {
            "date": "Aug. 17\n10 pm",
            "location": "Estadio Olímpico Universitário",
            "home_team": "Pumas UNAM (MEX)",
            "away_team": "FC Dallas (USA)",
            "home_score": "0",
            "away_score": "1",
            "competition": "CONCACAF Champions League",
            "round": "Group Stage",
            "notes": "",
            "source": url,
            }
        assert games[5] == another_game


    def test_mls_concacaf_stats():
        url = 'http://www.mlssoccer.com/matchcenter/2011-08-16-la-galaxy-vs-motagua/stats'

        goals = [
            {'club': 'LA', 'name': 'Adam Cristman', 'time': '13'},
            {'club': 'LA', 'name': 'Landon Donovan', 'time': '60'},
            ]

        assists = [
            {'club': 'LA', 'name': 'A.J. DeLaGarza', 'time': '13'},
            {'club': 'LA', 'name': 'David Beckham', 'time': '60'},
            ]

        positions = [   
            'POS',
            'Player',
            'MIN',
            'G',
            'A',
            'SHT',
            'SOG',
            'CK',
            'OF',
            'FC',
            'FS',
            ]

        stats = []

        l = ['4', 'D', 'Omar Gonzalez', '90', '0', '0', '3', '1', '0', '0', '1', '1']

        '10FLandon Donovan9010331122'
        '12MIvan Guerrero7000000011'


"""
