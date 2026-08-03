# A standings object. Used to generate standings.
#
# Not currently wired into the build: generate.py has its own rolling Standing
# class, and imports get_standings without calling it. Kept for the checking
# work in ROADMAP.md, which wants a table to compare loaded standings against.

from collections import defaultdict


def get_standings(games, competition, season):
    return Standing(games, competition, season).standings()


class Standing(object):

    def __init__(self, games, competition, season):
        self.competition = competition
        self.season = season

        self.teams = set()
        self.wins = defaultdict(int)
        self.losses = defaultdict(int)
        self.ties = defaultdict(int)
        self.goals_for = defaultdict(int)
        self.goals_against = defaultdict(int)

        # One pass: `games` may be a cursor.
        for game in games:
            self.add_game(game)

    def add_game(self, game):
        home, away = game['home_team'], game['away_team']
        h, a = game['home_score'], game['away_score']

        self.teams.update((home, away))

        self.goals_for[home] += h
        self.goals_against[home] += a
        self.goals_for[away] += a
        self.goals_against[away] += h

        if h == a:
            self.ties[home] += 1
            self.ties[away] += 1
        elif h > a:
            self.wins[home] += 1
            self.losses[away] += 1
        else:
            self.wins[away] += 1
            self.losses[home] += 1

    def points(self, team):
        return 3 * self.wins[team] + self.ties[team]

    def standings(self):
        rows = [{
            'name': team,
            'wins': self.wins[team],
            'losses': self.losses[team],
            'ties': self.ties[team],
            'points': self.points(team),
            'goals_for': self.goals_for[team],
            'goals_against': self.goals_against[team],
            'competition': self.competition,
            'season': self.season,
        } for team in sorted(self.teams)]

        return sorted(rows, key=lambda d: -d['points'])
