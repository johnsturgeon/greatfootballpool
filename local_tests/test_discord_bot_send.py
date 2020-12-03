#!/usr/bin/env python
"""Unit Test wrapper for discord_bot_tester.py"""
import os
import init
settings = init.get_settings()

import discord.bot_send as discord_bot

def test_send_embed():
    discord_bot.send_message("Hello")