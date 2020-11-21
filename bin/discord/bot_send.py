#!/usr/bin/env python
"""Discord bot runs in the background and handles all requests to discord."""
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
import discord  # noqa E402
from discord import Guild  # noqa W291

client = discord.Client()
TOKEN = settings['discord']['token']


@client.event
async def on_ready():
    guild_name = settings['discord']['guild']
    guild: Guild
    for guild in client.guilds:
        if guild.name == guild_name:
            break
    channel = None
    for channel in guild.channels:
        if channel.name == "tgfp-bot-chat":
            break
    await channel.send("Hi")
    await client.close()


client.run(TOKEN)
