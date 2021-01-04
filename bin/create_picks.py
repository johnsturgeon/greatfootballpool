""" Used to create the picks page """
import pprint
from yahoo import Yahoo
from tgfp import TGFP, TGFPGame

pp = pprint.PrettyPrinter(indent=4)
tgfp = TGFP()
tgfp_teams = tgfp.teams()
week_no = tgfp.current_week()
yahoo = Yahoo(week_no=week_no)
yahoo_games = yahoo.games()
teams = yahoo.teams()


def round_to(number, precision):
    """ rounds a given number to a given precision """
    correction = 0.5 if number >= 0 else -0.5
    return int(number / precision + correction) * precision


def main():
    """ Runs the main method to create the picks page """
    print("Current week: %d" % week_no)
    for yahoo_game in yahoo_games:
        print("yahoo_game_id: " + yahoo_game.id)
        print(yahoo_game.away_team.full_name)
        road_team_id = yahoo_game.away_team.tgfp_id(tgfp_teams)
        home_team_id = yahoo_game.home_team.tgfp_id(tgfp_teams)
        print("road_team_id: " + str(road_team_id))
        print(yahoo_game.home_team.full_name)
        print("home_team_id: " + str(home_team_id))
        average_spread = yahoo_game.average_home_spread()
        print(average_spread)
        if average_spread is None:
            average_spread = 0
        if average_spread < 0:
            if average_spread > -0.5:
                average_spread = -0.5
            favorite_team_id = home_team_id
        elif average_spread > 0:
            if average_spread < 0.5:
                average_spread = 0.5
            favorite_team_id = road_team_id
        else:
            favorite_team_id = home_team_id
            average_spread = 0.5
        average_spread = round_to(abs(average_spread), .5)
        tgfp_game = TGFPGame(tgfp=tgfp)
        tgfp_game.favorite_team_id = favorite_team_id
        tgfp_game.game_status = yahoo_game.status_type

        tgfp_game.home_team_id = home_team_id
        tgfp_game.home_team_score = 0
        tgfp_game.road_team_id = road_team_id
        tgfp_game.road_team_score = 0
        tgfp_game.spread = float(average_spread)
        tgfp_game.start_time = yahoo_game.start_time
        tgfp_game.week_no = int(week_no)
        tgfp_game.yahoo_game_id = yahoo_game.id
        tgfp_game.season = tgfp.current_season()
        print("Saving game in mongo database")
        pp.pprint(tgfp_game.mongo_data())
        tgfp_game.save()
        print("")


if __name__ == "__main__":
    main()
