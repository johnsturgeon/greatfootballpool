#!../env/bin/python
""" Updates the win/loss record for all the players in TGFP """
from yahoo import Yahoo
from tgfp import TGFP


def main():
    """ Main function for running the entire file """
    tgfp = TGFP()
    yahoo = Yahoo(tgfp.current_week())

    last_week = tgfp.last_week_completed()
    active_players = tgfp.find_players(player_active=True)

    for player in active_players:
        print("Working on %s" % player.nick_name)
        picks = tgfp.find_picks(player_id=player.id)
        total_wins = 0
        total_losses = 0
        total_bonus = 0
        total_last_wins = 0
        total_last_losses = 0
        total_last_bonus = 0
        for pick in picks:
            pick.load_record()
            pick.save()
            total_wins += pick.wins
            total_losses += pick.losses
            total_bonus += pick.bonus
            if pick.week_no == last_week:
                total_last_wins += pick.wins
                total_last_losses += pick.losses
                total_last_bonus += pick.bonus

        print("Total wins " + str(total_wins))
        print("Total losses " + str(total_losses))
        print("Total bonus " + str(total_bonus))
        print("Total last week wins " + str(total_last_wins))
        print("Total last week losses " + str(total_last_losses))
        print("Total last week bonus " + str(total_last_bonus))
        player.wins = total_wins
        player.losses = total_losses
        player.bonus = total_bonus
        player.last_wins = total_last_wins
        player.last_losses = total_last_losses
        player.last_bonus = total_last_bonus

    for yahoo_team in yahoo.teams():
        tgfp_team = tgfp.find_teams(yahoo_team_id=yahoo_team.id)[0]
        tgfp_team.wins = yahoo_team.wins
        tgfp_team.losses = yahoo_team.losses
        tgfp_team.ties = yahoo_team.ties
        tgfp_team.logo_url = yahoo_team.logo_url
        tgfp_team.save()


if __name__ == "__main__":
    main()
