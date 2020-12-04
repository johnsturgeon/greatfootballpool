#!/usr/bin/env python
"""Unit Test wrapper for discord_bot_tester.py"""
import init
settings = init.get_settings()
# pylint: disable=wrong-import-position
import bot_send as discord_bot


def test_send_embed():
    """
    Stubbed out for now, but will eventually test sending a message to discord
    """
    discord_bot.send_message("Hello")
