#!../env/bin/python
"""Discord bot runs in the background and handles all requests to discord."""
import os
import logging
import json
from tgfp import TGFP
import discord
from discord import Guild

client = discord.Client()

# TODO: replace this with `bot_send`


class MessageData():
    """This class will contain all the data necessary to send the message."""

    # pylint: disable=too-few-public-methods
    # pylint: disable=missing-function-docstring
    def __init__(self):
        self.__game_id = None

    @property
    def game_id(self):
        return self.__game_id

    @game_id.setter
    def game_id(self, game_id):
        self.__game_id = game_id


message_data = MessageData()


def embed_game_alert():
    """ Creates the embedded game alert message
    Returns:
       embed: discord Embed object
    """
    tgfp = TGFP()
    game_id = message_data.game_id
    game = tgfp.find_games(game_id=game_id)[0]
    winning_team = game.winning_team
    losing_team = game.losing_team
    winning_players_string = ""
    losing_players_string = ""
    for player in tgfp.find_players(player_active=True):
        if player.this_weeks_picks() is None:
            break
        # if player.picked_winner_of_final_game(game_id):
        #     bonus = player.lock_pick_points_final_game(game_id)
        #     bonus += player.upset_pick_points_final_game(game_id)
        #     winning_players_string += f"{player.nick_name}"
        #     if bonus != 0:
        #         winning_players_string += f" ({bonus:+})"
        #     winning_players_string += "\n"
        # else:
        #     bonus = player.lock_pick_points_final_game(game_id)
        #     losing_players_string += f"{player.nick_name}"
        #     if bonus != 0:
        #         losing_players_string += f" ({bonus:+})"
        #     losing_players_string += "\n"

    embed = discord.Embed(
        title="GAME ALERT",
        description=f'''{winning_team.full_name} have defeated the {losing_team.full_name}
 by a score of {game.winning_team_score} - {game.losing_team_score}''',
        color=0x00ff00)
    embed.set_thumbnail(url=winning_team.logo_url)
    embed.add_field(name="Winners", value=winning_players_string, inline=True)
    embed.add_field(name="Losers", value=losing_players_string, inline=True)
    embed.set_footer(text="(+/-n) after name indicates bonus points")
    return embed


@client.event
async def on_ready():
    """ callback for when discord bot connects to the channel and is ready """
    guild: Guild
    for guild in client.guilds:
        if guild.name == os.getenv('DISCORD_GUILD'):
            break
    channel = None
    for channel in guild.channels:
        if channel.name == "tgfp-bot-chat":
            break
    await channel.send(embed=embed_game_alert())
    logging.debug("Sent Game Alert")
    await client.close()


def alert_game_id_final(tgfp_game_id):
    """ called from an external program to send a game alert """
    dirname = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(dirname, '../conf/settings.json'))
    with open(conf_path) as config_file:
        settings = json.load(config_file)
    log_dir = settings['config']['log_dir']
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename=f"{log_dir}/bot_send.log",
                        filemode='w')

    token = settings['discord']['token']
    message_data.game_id = tgfp_game_id
    logging.debug('Got a game alert request for game: %s', tgfp_game_id)
    client.run(token)
