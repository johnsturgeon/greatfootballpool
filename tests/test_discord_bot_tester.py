#!/usr/bin/env python
"""Unit Test wrapper for discord_bot_tester.py"""
import os
import init
settings = init.get_settings()
discord_bot_user_id = settings['discord']['discord_bot_user_id']
test_token = settings['discord']['test_token']
bot_chat_channel_id = settings['discord']['test_bot_chat_channel_id']


def get_command(bot_test_to_run="all"):
    dirname = os.path.dirname(os.path.abspath(__file__))
    fullpath = f"{dirname}/discord_bot_tester.py"
    fullpath += f" {discord_bot_user_id} {test_token} -c {bot_chat_channel_id}"
    fullpath += f" -r {bot_test_to_run}"
    return fullpath


# def test_hearbeat(bash):
#     assert 'CLI' in bash.run_script_inline([get_command('test_heartbeat')])


# def test_this_week(bash):
#     assert 'CLI' in bash.run_script_inline([get_command('test_this_week')])


# def test_standings(bash):
#     assert 'CLI' in bash.run_script_inline([get_command('test_standings')])
