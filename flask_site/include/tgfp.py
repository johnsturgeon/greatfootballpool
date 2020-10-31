"""
  This module contains all of the necessary functions for interfacing with
  the the great football pool mongo database
"""
import os
import pprint
from pymongo import MongoClient
import pytz
from yahoo import Yahoo
from dotenv import load_dotenv

dirname = os.path.dirname(os.path.abspath(__file__))
DOT_ENV_PATH = os.path.normpath(os.path.join(dirname, '../../conf/.env'))
load_dotenv(dotenv_path=DOT_ENV_PATH)
pp = pprint.PrettyPrinter(indent=4)


# pylint: disable=missing-function-docstring
class TGFP():
    """
    Main class for the great football pool
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        # traceback.print_stack(file=sys.stdout)
        self.init_ivars()
        self.mongoclient = MongoClient(
            os.getenv('MONGO_DB_URL'))
        self.mongodb = self.mongoclient['tgfp']
        self._yahoo = None
        self._home_page_text = None
        self._last_week_completed = None
        self._current_season = None

    def games(self):
        """
        Get an array of all TGFPGames in the entire db
        Returns:
          - TGFPGames[]
        """
        if not self._games:
            for game in self.mongodb.games.find(batch_size=100000):
                self._games.append(TGFPGame(tgfp=self, data=game))
        return self._games

    def teams(self):
        if not self._teams:
            for team in self.mongodb.teams.find(batch_size=100000):
                self._teams.append(TGFPTeam(tgfp=self, data=team))
        return self._teams

    def picks(self):
        if not self._picks:
            for pick in self.mongodb.picks.find(batch_size=100000):
                self._picks.append(TGFPPick(tgfp=self, data=pick))
        return self._picks

    def players(self):
        if not self._players:
            for player in self.mongodb.players.find(batch_size=100000):
                self._players.append(TGFPPlayer(tgfp=self, data=player))
        return self._players

    def yahoo(self):
        if not self._yahoo:
            self._yahoo = Yahoo(week_no=0)
        return self._yahoo

    def current_week(self):
        last_game: TGFPGame
        current_week: int
        last_game = self.find_games(ordered_by='week_no')[-1]
        last_weeks_games = self.find_games(week_no=last_game.week_no)
        all_games_completed = True
        game: TGFPGame
        for game in last_weeks_games:
            if game.game_status != 'final':
                all_games_completed = False
                break
        if all_games_completed:
            current_week = game.week_no + 1
        else:
            current_week = game.week_no

        return current_week

    def home_page_text(self):
        if not self._home_page_text:
            tgfp_info = self.mongodb.tgfp_info.find_one(batch_size=100000)
            self._home_page_text = tgfp_info['home_page_text']
        return self._home_page_text

    def last_week_completed(self):
        return self.current_active_week()

    def current_season(self):
        if not self._current_season:
            current_season = self.mongodb.tgfp_info.find_one(batch_size=100000)
            self._current_season = current_season['current_season']
        return self._current_season

    def current_active_week(self):
        last_game: TGFPGame
        current_week: int
        last_game = self.find_games(ordered_by='week_no')[-1]
        last_weeks_games = self.find_games(week_no=last_game.week_no)
        any_games_completed = False
        game: TGFPGame
        for game in last_weeks_games:
            if game.game_status == 'final':
                any_games_completed = True
                break
        if any_games_completed:
            current_week = game.week_no
        else:
            current_week = game.week_no - 1

        return current_week

    def find_players(
            self,
            player_id=None,
            player_email=None,
            discord_id=None,
            player_active=None,
            ordered_by=None,
            reverse_order=False):
        # pylint: disable=too-many-arguments
        """
        Returns a list of players based on the search criteria
        Args:
           - _id: ID of the player
           - player_email: string: search by player email
           ...
        Returns:
          TGFPlayer[] or empty list [] if none are found
        """

        found_players = []
        player: TGFPPlayer
        for player in self.players():
            found = True
            if player_id and player_id != player.id:
                found = False
            if player_email and player_email != player.email:
                found = False
            if player_active and player_active != player.active:
                found = False
            if discord_id and discord_id != player.discord_id:
                found = False
            if found:
                found_players.append(player)
        if ordered_by == "total_points":
            found_players.sort(key=lambda x: x.total_points(), reverse=reverse_order)

        return found_players

    def find_teams(self, team_id=None, yahoo_team_id=None):
        found_teams = []
        team: TGFPTeam
        for team in self.teams():
            found = True
            if team_id and team_id != team.id:
                found = False
            if yahoo_team_id and yahoo_team_id != team.yahoo_team_id:
                found = False
            if found:
                found_teams.append(team)

        return found_teams

    def find_picks(self, pick_id=None, week_no=None, season=None, player_id=None):
        found_picks = []
        if season:
            search_season = season
        else:
            search_season = self.current_season()

        pick: TGFPPick
        for pick in self.picks():
            found = True
            if pick_id and pick_id != pick.id:
                found = False
            if week_no and week_no != pick.week_no:
                found = False
            if search_season != pick.season:
                found = False
            if player_id and player_id != pick.player_id:
                found = False
            if found:
                found_picks.append(pick)

        return found_picks

    def find_games(
            self, game_id=None,
            yahoo_game_id=None,
            week_no=None, season=None,
            home_team_id=None,
            ordered_by=None,
            game_status=None):
        # pylint: disable=too-many-arguments

        found_games = []
        if season:
            search_season = season
        else:
            search_season = self.current_season()
        game: TGFPGame
        for game in self.games():
            found = True
            if game_id and game_id != game.id:
                found = False
            if yahoo_game_id and yahoo_game_id != game.yahoo_game_id:
                found = False
            if week_no and week_no != game.week_no:
                found = False
            if search_season != game.season:
                found = False
            if home_team_id and home_team_id != game.home_team_id:
                found = False
            if game_status and game_status != game.game_status:
                found = False
            if found:
                found_games.append(game)

        if ordered_by == "start_time":
            found_games.sort(key=lambda x: x.start_time)
        if ordered_by == "week_no":
            found_games.sort(key=lambda x: x.week_no)

        return found_games

    def init_ivars(self):
        self._teams = []
        self._games = []
        self._picks = []
        self._players = []
        self._last_week_completed = 0
        self._home_page_text = ""
        self._current_season = 0
        self._yahoo = None


class TGFPTeam():
    # pylint: disable=too-many-instance-attributes
    """
    TGFP Class for a 'team'
    """
    def __init__(self, tgfp, data):
        self._tgfp = tgfp
        self._id = data['_id']
        self.short_name = data['short_name']
        self.city = data['city']
        self.long_name = data['long_name']
        self.wins = int(data['wins'])
        self.losses = int(data['losses'])
        self.ties = int(data['ties'])
        self.yahoo_team_id = data['yahoo_team_id']
        self.logo_url = data['logo_url']
        self.full_name = self.city + ' ' + self.long_name

    def mongo_data(self):
        filtered_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                filtered_dict.update({key: value})

        return filtered_dict

    def save(self):
        self._tgfp.mongodb.teams.update_one(
            {
                "_id": self._id
            },
            {"$set": self.mongo_data()}
        )

    @property
    def id(self):
        # pylint: disable=invalid-name
        return self._id


class TGFPPlayer():
    # pylint: disable=too-many-instance-attributes
    """ Class for a player """
    def __init__(self, tgfp, data):
        self._tgfp = tgfp
        self._picks = None
        self._id = data['_id']
        self.last_name = data['last_name']
        self.first_name = data['first_name']
        self.nick_name = data['nick_name']
        self.email = data['email']
        self.password = data['password']
        self.active = bool(data['active'])
        self.discord_id = data['discord_id']

    @property
    def id(self):
        # pylint: disable=invalid-name
        return self._id

    def wins(self, week_no=None):
        if not self._picks:
            self.load_picks()
        wins = 0
        for pick in self._picks:
            if not week_no or pick.week_no == week_no:
                wins += pick.wins
        return wins

    def losses(self, week_no=None):
        if not self._picks:
            self.load_picks()
        losses = 0
        for pick in self._picks:
            if not week_no or pick.week_no == week_no:
                losses += pick.losses
        return losses

    def bonus(self, week_no=None):
        if not self._picks:
            self.load_picks()
        bonus = 0
        for pick in self._picks:
            if not week_no or pick.week_no == week_no:
                bonus += pick.bonus
        return bonus

    def last_bonus(self):
        return self.bonus(week_no=self._tgfp.last_week_completed())

    def total_points(self):
        return self.wins() + self.bonus()

    def last_wins(self):
        return self.wins(week_no=self._tgfp.last_week_completed())

    def last_losses(self):
        return self.losses(week_no=self._tgfp.last_week_completed())

    def load_picks(self):
        self._picks = self._tgfp.find_picks(player_id=self._id)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def winning_pct(self):
        wins_and_losses = float(self.wins() + self.losses())
        if wins_and_losses:
            return self.wins() / wins_and_losses

        return 0

    def this_weeks_picks(self):
        picks = self._tgfp.find_picks(player_id=self._id, week_no=self._tgfp.current_week())
        if picks:
            return picks[0]

        return None

    def picked_winner_of_final_game(self, tgfp_game_id):
        game: TGFPGame
        game = self._tgfp.find_games(game_id=tgfp_game_id)[0]
        assert game.game_status == 'final'
        picks = self.this_weeks_picks()
        assert picks, "We should have picks"
        for pick in picks.pick_detail:
            if pick['game_id'] == game.id:
                return game.winner_id_of_game == pick['winner_id']

        return False

    def lock_pick_points_final_game(self, tgfp_game_id):
        """
        Given a game, how many 'lock' points
        Args:
             tgfp_game_id: str the game to check
            game status must be 'final'
        Returns:
            - int: -1, 0, or 1
        Note:
            -1 indicates lost lock point
            0 indicates no lock
            1 indicates won lock
        Note:
            The method will assert if the game is not final
        """

        game = self._tgfp.find_games(game_id=tgfp_game_id)[0]
        assert game.game_status == 'final'
        picks = self.this_weeks_picks()
        lock_points = 0
        # first let's figure out if the game.winner_team_id is equal to the lock
        if game.winner_id_of_game == picks.lock_team_id:
            if self.picked_winner_of_final_game(tgfp_game_id):
                lock_points = 1
            else:
                lock_points = -1

        return lock_points

    # Returns 0 or 1
    # 0 indicates no upset
    # 1 indicates won upset
    def upset_pick_points_final_game(self, tgfp_game_id):
        game = self._tgfp.find_games(game_id=tgfp_game_id)[0]
        assert game.game_status == 'final'
        picks = self.this_weeks_picks()
        # first let's figure out if the game_id is equal to the upset
        pick_points = 0
        if game.winner_id_of_game == picks.upset_team_id:
            pick_points = 1

        return pick_points

    def mongo_data(self):
        filtered_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                filtered_dict.update({key: value})

        return filtered_dict

    def save(self):
        self._tgfp.mongodb.players.update_one(
            {
                "_id": self._id
            },
            {"$set": self.mongo_data()},
            upsert=True
        )


class TGFPGame():
    # pylint: disable=too-many-instance-attributes
    """ Game class for the TGFP """
    def __init__(self, tgfp, data=None):
        self._tgfp = tgfp
        self._id = None

        if data:
            self.load_data(data)

    def mongo_data(self):
        filtered_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                filtered_dict.update({key: value})

        return filtered_dict

    def load_data(self, data):
        if '_id' in data:
            self._id = data['_id']
        # below are mandatory fields in the DB
        self.favorite_team_id = data['favorite_team_id']
        self.game_status = data['game_status']
        self.home_team_id = data['home_team_id']
        self.home_team_score = data['home_team_score']
        self.road_team_id = data['road_team_id']
        self.road_team_score = data['road_team_score']
        self.spread = data['spread']
        self.start_time = data['start_time']
        self.week_no = data['week_no']
        self.season = data['season']
        self.yahoo_game_id = data['yahoo_game_id']

    def save(self):
        result = self._tgfp.mongodb.games.update_one(
            {
                "yahoo_game_id": self.yahoo_game_id
            },
            {"$set": self.mongo_data()},
            upsert=True
        )
        if result.upserted_id:
            self._id = result.upserted_id
        else:
            found_games = self._tgfp.find_games(yahoo_game_id=self.yahoo_game_id)
            found_game: TGFPGame
            found_game = found_games[0]
            self._id = found_game.id
        assert self._id is not None

    @property
    def id(self):
        # pylint: disable=invalid-name
        return self._id

    @property
    def winner_id_of_game(self):
        winner_id = None
        if self.game_status == 'final':
            if self.home_team_score > self.road_team_score:
                winner_id = self.home_team_id
            elif self.road_team_score > self.home_team_score:
                winner_id = self.road_team_id

        return winner_id

    @property
    def leader_id_of_game(self):
        leader_id = None
        if self.home_team_score > self.road_team_score:
            leader_id = self.home_team_id
        elif self.road_team_score > self.home_team_score:
            leader_id = self.road_team_id

        return leader_id

    @property
    def loser_id_of_game(self):
        loser_id = None
        if self.game_status == 'final':
            if self.home_team_score > self.road_team_score:
                loser_id = self.road_team_id
            elif self.road_team_score > self.home_team_score:
                loser_id = self.home_team_id

        return loser_id

    @property
    def winning_team(self):
        if self.game_status == 'final':
            return self._tgfp.find_teams(team_id=self.winner_id_of_game)[0]

        return None

    @property
    def losing_team(self):
        if self.game_status == 'final':
            return self._tgfp.find_teams(team_id=self.loser_id_of_game)[0]

        return None

    @property
    def winning_team_score(self):
        winning_team_score = None
        assert self.game_status == 'final'
        if self.home_team_score > self.road_team_score:
            winning_team_score = self.home_team_score
        elif self.road_team_score > self.home_team_score:
            winning_team_score = self.road_team_score

        return winning_team_score

    @property
    def losing_team_score(self):
        assert self.game_status == 'final'
        losing_team_score = None
        if self.home_team_score > self.road_team_score:
            losing_team_score = self.road_team_score
        elif self.road_team_score > self.home_team_score:
            losing_team_score = self.home_team_score

        return losing_team_score

    @property
    def road_team(self):
        return self._tgfp.find_teams(team_id=self.road_team_id)

    @property
    def home_team(self):
        return self._tgfp.find_teams(team_id=self.home_team_id)

    @property
    def underdog_team_id(self):
        if self.favorite_team_id == self.home_team_id:
            return self.road_team_id

        return self.home_team_id

    @property
    def pacific_start_time(self):
        utc_dt = self.start_time.replace(tzinfo=pytz.utc)
        pac_dt = pytz.timezone('US/Pacific')
        return pac_dt.normalize(utc_dt.astimezone(pac_dt))


class TGFPPick():
    """ Class for the player's picks """
# pylint: disable=too-many-instance-attributes
# pylint: enable=too-many-instance-attributes
    def __init__(self, tgfp, data):
        self._tgfp = tgfp
        self._id = None
        if data:
            if '_id' in data:
                self._id = data['_id']
            self.lock_team_id = data['lock_team_id']
            self.player_id = data['player_id']
            self.upset_team_id = data['upset_team_id']
            self.week_no = data['week_no']
            self.season = data['season']
            self.wins = data['wins']
            self.losses = data['losses']
            self.bonus = data['bonus']
            self.pick_detail = data['pick_detail']
        else:
            self.wins = 0
            self.losses = 0
            self.bonus = 0
            self.upset_team_id = None
            self.season = tgfp.current_season()

    def winner_for_game_id(self, game_id):
        winner_id = None
        for pick in self.pick_detail:
            if pick['game_id'] == game_id:
                winner_id = pick['winner_id']
                break
        return winner_id

    def load_record(self, games=None):
        # go through each game in pick_detail
        self.wins = 0
        self.losses = 0
        self.bonus = 0

        games_array = self._tgfp.find_games(
                            week_no=self.week_no,
                            season=self.season) if games is None else games

        pick: TGFPPick
        for pick in self.pick_detail:
            game: TGFPGame
            for game in games_array:
                if game.id == pick['game_id']:
                    break
            if game.game_status == "final":
                if game.road_team_score == game.home_team_score:
                    winning_team_id = None
                    self.losses += 1
                else:
                    if game.road_team_score > game.home_team_score:
                        winning_team_id = game.road_team_id
                        losing_team_id = game.home_team_id
                    else:
                        winning_team_id = game.home_team_id
                        losing_team_id = game.road_team_id

                    self.update_wins(pick, winning_team_id)
                    self.update_bonus(winning_team_id, losing_team_id)

    def update_wins(self, pick, winning_team_id):
        if winning_team_id == pick['winner_id']:
            self.wins += 1
        else:
            self.losses += 1

    def update_bonus(self, winning_team_id, losing_team_id):
        if winning_team_id == self.lock_team_id:
            self.bonus += 1
        if losing_team_id == self.lock_team_id:
            self.bonus -= 1
        if winning_team_id == self.upset_team_id:
            self.bonus += 1

    def save(self):
        result = self._tgfp.mongodb.picks.update_one(
            {
                "player_id": self.player_id,
                "week_no": self.week_no,
                "season": self.season
            },
            {"$set": self.mongo_data()},
            upsert=True
        )
        if result.upserted_id:
            self._id = result.upserted_id
        assert self._id is not None

# pylint: disable=invalid-name
    @property
    def id(self):
        return self._id
# pylint: enable=invalid-name

    def mongo_data(self):
        filtered_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                filtered_dict.update({key: value})

        return filtered_dict
