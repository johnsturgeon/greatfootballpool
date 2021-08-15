"""Discord bot runs in the background and handles all requests to discord."""
import os
import logging
import discord
from include.tgfp import TGFP, TGFPGame, TGFPPick, TGFPPlayer
from instance.config import get_config

config = get_config(os.getenv('FLASK_ENV'))
logger = config.logger(os.path.basename(__file__))

TOKEN = config.DISCORD_TOKEN
GUILD = config.DISCORD_GUILD
WEBHOOK_BOT_ID = config.DISCORD_WEBHOOK_BOT_ID
ADMIN_EMAIL = config.DISCORD_ADMIN_EMAIL

client = discord.Client()
tgfp = TGFP()


def game_line_for_game(tgfp_game: TGFPGame, player_pick: TGFPPick):
    """
      This method should return back all the values necessary
      for a formatted printed output of a game
      Args:
        - tgfp_game: `TGFPGame` to query
        - player_pick: the `TGFPPick` object for the current player

      Returns:
        - tuple: (road_team.short_name,
                  home_team.short_name,
                  player_win_team.short_name,
                  winning_team,
                  tgfp_game.road_team_score,
                  tgfp_game.home_team_score,
                  icon)
      """

    # first let's figure out if we have a winner (final game)
    road_team = tgfp.find_teams(tgfp_game.road_team_id)[0]
    home_team = tgfp.find_teams(tgfp_game.home_team_id)[0]
    player_win_team = tgfp.find_teams(player_pick.winner_for_game_id(tgfp_game.id))[0]
    final = tgfp_game.game_status == 'final'
    if tgfp_game.game_status != 'pregame':
        if tgfp_game.leader_id_of_game is None:
            winning_team = '---'
            icon = '🟠'
        else:
            winning_team = tgfp.find_teams(tgfp_game.leader_id_of_game)[0].short_name
            if winning_team == player_win_team.short_name:
                icon = '✅' if final else '👍'
            else:
                icon = '☠️' if final else '🙏'
    else:
        winning_team = None
        icon = '⚫️'

    return [
        road_team.short_name,
        home_team.short_name,
        player_win_team.short_name,
        winning_team,tgfp_game.road_team_score,
        tgfp_game.home_team_score,
        icon
    ]


def help_message():
    """ simply returns the help message """
    help_msg = '''
```
TGFP Command List:
==================

!TGFP Standings
  - prints the current standings
!TGFP This Week
  - prints your score for the current week

(coming soon)
!TGFP Scores
  - print the current scores
```
'''
    return help_msg


def test_message():
    """ This is just for testing """
    test_msg = "💗💗💗💗💗"
    return test_msg


def this_week(message) -> str:
    # pylint: disable=too-many-locals
    """ returns message for the player's record for the current week """
    player: TGFPPlayer = tgfp.find_players(player_email=ADMIN_EMAIL)[0]
    players = tgfp.find_players(discord_id=message.author.id)
    if players:
        player = players[0]
    elif message.author.id != WEBHOOK_BOT_ID:
        assert False

    logging.info("%s just asked for !TGFP This Week", player.nick_name)
    week_no = tgfp.current_active_week()
    games = tgfp.find_games(week_no=week_no, ordered_by='start_time')
    output = "```\n"
    output += f"Results for {player.nick_name} (Week {week_no}):\n"
    output += "🏈   Game   | Pick |  Win (score)\n"
    output += "=================================\n"
    player_pick = tgfp.find_picks(player_id=player.id, week_no=week_no)[0]
    wins = 0
    losses = 0
    potential_wins = 0
    potential_losses = 0
    if not player_pick:
        output += "No picks yet"
    else:
        for game in games:
            road, home, pick, winner, road_score, home_score, icon = \
                game_line_for_game(game, player_pick)
            output += f"{icon} {road:>3} @ {home:>3} | {pick:>3}"
            if winner:
                output += f" | {winner:<3} ({road_score}-{home_score})"
            output += "\n"
            if icon == '✅':
                wins += 1
            if icon == '👍':
                potential_wins += 1
            if icon == '☠️':
                losses += 1
            if icon == '🙏':
                potential_losses += 1

    output += f"\nRecord: ({wins}-{losses})\n"
    output += f"Potential Record: ({wins + potential_wins}-{losses + potential_losses})\n"
    output += "=================================\n"
    output += "⚫ = Not Started\n👍 = In Progress (winning)\n🙏 =" + \
              " In Progress (losing)\n✅ = You Won\n☠️ = You Lost\n"
    output += "```\n"
    logging.info('Sending Results for !TGFP This Week to %s', {player.nick_name})
    return output


@client.event
async def on_ready():
    # pylint: disable=missing-function-docstring
    guild = None
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    logging.info(
        '%s is connected to the following guild: %s (id: %s)',
        {client.user},
        {guild.name},
        {guild.id}
    )
    members = ""
    for member in guild.members:
        members += "\n -" + member.display_name + " : " + str(member.id)
    logging.info("Guild Members:\n - %s", members)


@client.event
async def on_message(message):
    # pylint: disable=missing-function-docstring
    if message.author == client.user:
        return
    # if message.channel.name != 'tgfp-bot-chat':
    #     await message.channel.send('Please use `#tgfp-bot-chat` to talk to me')
    #     return
    if message.content == '!TGFP Scores':
        await message.channel.send("No Scores Yet")
    if message.content == '!TGFP Standings':
        active_players = tgfp.find_players(
            player_active=True,
            ordered_by="total_points",
            reverse_order=True)
        name_len = 0
        for player in active_players:
            name_len = max(name_len, len(player.nick_name))
        output = "```\n"
        header = f"{'Name':^{name_len}}|  W  |  L  |Bonus| GB\n"
        header_len = len(header)
        output += header
        output += "".ljust(header_len, "=") + "\n\n"
        for player in active_players:
            games_back = active_players[0].total_points() - player.total_points()
            player_record = \
                f"{player.nick_name:<{name_len}}|{player.wins():^5}|" + \
                f"{player.losses():^5}|{player.bonus():^5}|{games_back:>3}\n"
            output += player_record

        output += "```\n"
        output += "See more here: https://greatfootballpool.com/standings"
        await message.channel.send(output)

    if message.content == '!TGFP This Week':
        await message.channel.send(this_week(message))

    if message.content == '!TGFP Help':
        await message.channel.send(help_message())

    if message.content == '!TGFP Test':
        await message.channel.send(test_message())


client.run(TOKEN)
