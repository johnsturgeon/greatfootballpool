""" This file will update all the scores in the mongo DB for the great football pool """
import os
import pprint
from instance.config import get_config
from include.yahoo import Yahoo
from include.tgfp import TGFP

config = get_config(os.getenv('FLASK_ENV'))
logger = config.logger(os.path.basename(__file__))


def main():
    """ This is the function runs the entire module. """
    pretty_printer = pprint.PrettyPrinter(indent=4)
    tgfp = TGFP()
    week_no = tgfp.current_week()
    yahoo = Yahoo(week_no=week_no)
    yahoo_games = yahoo.games()
    all_games_are_final = True

    for yahoo_g in yahoo_games:
        if yahoo_g.status_type == "postponed":
            continue
        if yahoo_g.status_type != "pregame":
            tgfp_g = tgfp.find_games(yahoo_game_id=yahoo_g.id)[0]
            print("Games are in progress")
            if tgfp_g:
                if tgfp_g.home_team_score != int(yahoo_g.total_home_points) or \
                   tgfp_g.road_team_score != int(yahoo_g.total_away_points) or \
                   tgfp_g.game_status != yahoo_g.status_type:
                    tgfp_g.home_team_score = int(yahoo_g.total_home_points)
                    tgfp_g.road_team_score = int(yahoo_g.total_away_points)
                    tgfp_g.game_status = yahoo_g.status_type
                    print("saving a game score")
                    pretty_printer.pprint(tgfp_g.mongo_data())
                    tgfp_g.save()
                    if yahoo_g.score_is_final:
                        print("Sending alert")
                        # bot_sender.alert_game_id_final(tgfp_g.id)

        if not yahoo_g.score_is_final:
            all_games_are_final = False

    if all_games_are_final:
        print("all games are final")


if __name__ == "__main__":
    main()
