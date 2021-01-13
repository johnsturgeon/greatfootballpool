"""
  This module contains all of the necessary functions for interfacing with
  yahoo for retrieving scores, schedule data, etc.
"""
from urllib.request import Request, urlopen
import re
import json
from dateutil import parser


class Yahoo:
    """ The main class for interfacing with Yahoo's json for sports """

    def __init__(self, week_no):
        self._games = []
        self._teams = []
        self.games_data = None
        self.teams_data = None
        self.week_no = week_no
        self.debug = True

    def games(self):
        """
        Returns:
            a list of all YahooGames in the json structure
        """
        if not self._games:
            all_headers = {'Host': 'sports.yahoo.com',
                           'Accept':
                           'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Connection': 'keep-alive',
                           'Accept-Language': 'en-us',
                           'DNT': '1',
                           'User-Agent':
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13)" + \
                            "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0  Safari/604.1.38'
                           }
            # pylint: disable=invalid-name
            # schedState matches the url variable
            schedule_state = 2
            # if we're in the playoffs, we need to bump the schedState variable to 3
            if self.week_no > 17:
                schedule_state = 3
            url_to_query = 'http://sports.yahoo.com/nfl/scoreboard/?dateRange=%(week_no)d&' +\
                'dateRangeDisplay=%(week_no)d&schedState=%(schedState)d' % {
                    'week_no': self.week_no, 'schedState': schedule_state
                }
            req = Request(url_to_query, headers=all_headers)
            raw_game_data = urlopen(req).read().decode('utf-8')
            games_data = None
            for line in raw_game_data.splitlines():
                if re.match(r'^root.App.main.*', line):
                    split_line = line.split(' = ')[1].rstrip(';')
                    all_data = json.loads(split_line)
                    games_data = all_data['context']['dispatcher']['stores']['GamesStore']['games']
                    if self.debug:
                        try:
                            with open('games_data.json', 'w') as outfile:
                                json.dump(games_data, outfile)
                        except IOError:
                            print('could not write games data to json')
                    break
            for game_key in games_data:
                if re.match(r'^nfl*', game_key):
                    self._games.append(YahooGame(self, game_data=games_data[game_key]))

        return self._games

    def teams(self):
        """
        Returns:
            a list of all YahooTeams
        """
        if not self._teams:
            all_headers = {'Host': 'sports.yahoo.com',
                           'Accept':
                           'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Connection': 'keep-alive',
                           'Accept-Language': 'en-us',
                           'DNT': '1',
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) " +\
                           "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0  Safari/604.1.38'
                           }
            req = Request('https://sports.yahoo.com/nfl/standings/', headers=all_headers)
            raw_teams_data = urlopen(req).read().decode('utf-8')
            teams_data = None
            for line in raw_teams_data.splitlines():
                if re.match(r'^root.App.main.*', line):
                    split_line = line.split(' = ')[1].rstrip(';')
                    all_data = json.loads(split_line)
                    teams_data = all_data['context']['dispatcher']['stores']['TeamsStore']['teams']
                    if self.debug:
                        try:
                            with open('team_data.json', 'w') as outfile:
                                json.dump(teams_data, outfile)
                        except IOError:
                            print('could not write team data to json file')
                    break
            # print(json.dumps(teams_data))
            for team_key in teams_data:
                if 'default_league' in teams_data[team_key] and \
                   teams_data[team_key]['default_league'] == "nfl":
                    self._teams.append(YahooTeam(self, team_data=teams_data[team_key]))

        return self._teams

    def find_games(self):
        """ There are currently no filters for this, so it just finds all games """
        return self.games()

    def find_teams(self, team_id=None):
        """ returns a list of all teams optionally filtered by a single team_id """
        found_teams = []
        for team in self.teams():
            found = True
            if team_id and team_id != team.id:
                found = False
            if found:
                found_teams.append(team)

        return found_teams


class YahooGame:
    """ A single game from the Yahoo json """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, yahoo, game_data):
        # pylint: disable=invalid-name
        self.id = game_data['gameid']
        # pylint: enable=invalid-name
        self.yahoo = yahoo
        self.game_data = game_data
        self.home_team = yahoo.find_teams(team_id=game_data['home_team_id'])[0]
        self.away_team = yahoo.find_teams(team_id=game_data['away_team_id'])[0]
        self.start_time = parser.parse(game_data['start_time'])
        self.winning_team = yahoo.find_teams(team_id=game_data['winning_team_id'])[0]
        self.total_home_points = game_data['total_home_points']
        self.total_away_points = game_data['total_away_points']
        self.score_is_final = game_data['status_type'] == "final"
        self.status_type = game_data['status_type']

        self._odds = []

    def odds(self):
        """
        Returns:
            all the 'odds' from the Yahoo JSON
        """
        if not self._odds:
            if 'odds' in self.game_data:
                for odd in self.game_data['odds']:
                    self._odds.append(
                        YahooOdd(yahoo=self.yahoo, odd_data=self.game_data['odds'][odd]))

        return self._odds

    def average_home_spread(self):
        """ Takes all the odds and averages them out """
        number_of_odds = len(self.odds())
        print("number of odds: %d" % number_of_odds)
        home_spread_total = 0.0
        average_spread = None
        if self.odds():
            for odd in self.odds():
                print(odd.data)
                if odd.home_spread:
                    home_spread_total += float(odd.home_spread)
            average_spread = home_spread_total / number_of_odds

        return average_spread


class YahooTeam:
    """ The class that wraps the Yahoo JSON for each team """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(self, yahoo, team_data):
        self.yahoo = yahoo
        self.data = team_data
# pylint: disable=invalid-name
        self.id = team_data['team_id']
# pylint: enable=invalid-name
        self.full_name = team_data['full_name']
        self.logo_url = team_data['sportacularLogo']
        if 'team_standing' in team_data:
            self.wins = team_data['team_standing']['team_record']['wins']
            self.losses = team_data['team_standing']['team_record']['losses']
            self.ties = team_data['team_standing']['team_record']['ties']
        else:
            self.wins = 0
            self.losses = 0
            self.ties = 0

    def tgfp_id(self, tgfp_teams):
        """
        Args:
            tgfp_teams: list of teams to loop through
        Returns:
            the tgfp_id for the current yahoo team, None if not found
        """
        found_team_id = None
        for team in tgfp_teams:
            if self.id == team.yahoo_team_id:
                found_team_id = team.id
                break
        return found_team_id


class YahooOdd:
    """ Wraps the yahoo json for each 'odd' (spread) """
    # pylint: disable=too-few-public-methods

    def __init__(self, yahoo, odd_data):
        self.yahoo = yahoo
        self.data = odd_data
        # pylint: disable=invalid-name
        self.id = odd_data['book_id']
        # pylint: enable=invalid-name
        self.home_spread = odd_data['home_spread']
