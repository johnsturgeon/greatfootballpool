"""Discord bot runs in the background and handles all requests to discord."""
import os
import discord
# pylint: disable=import-error
# pylint: disable=no-name-in-module
from instance.config import get_config

config = get_config(os.getenv('FLASK_ENV'))


def send_message(message):
    """Sends a message to the discord channel"""
    client = discord.Client()

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send(message)
        await client.close()

    token = config.DISCORD_TOKEN
    channel_id = config.DISCORD_BOT_CHANNEL_ID
    client.run(token)
