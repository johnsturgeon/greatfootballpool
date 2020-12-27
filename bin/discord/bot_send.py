#!/usr/bin/env python
"""Discord bot runs in the background and handles all requests to discord."""
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
import discord  # noqa E402


def send_message(message):

    client = discord.Client()

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send(message)
        await client.close()

    token = settings['discord']['token']
    channel_id = settings['discord']['bot_chat_channel_id']
    client.run(token)
