"""Unit Test wrapper for discord_bot_tester.py"""
import os
import sys
from common_init import get_settings
settings = get_settings()
discord_bot_user_id = settings['discord']['discord_bot_user_id']
test_token = settings['discord']['test_token']
bot_chat_channel_id = settings['discord']['bot_chat_channel_id']


def get_command(bot_test_to_run="all"):
    """
    Returns a python command to run for testing the discord bot via the command line

    :param bot_test_to_run: Method to run in the `discord_bot_tester`
    :type bot_test_to_run: str
    :return: Full path to the command to run
    :rtype: str
    """
    interp = sys.executable
    dirname = os.path.dirname(os.path.abspath(__file__))
    full_path = interp
    full_path += f" {dirname}/discord_bot_tester.py"
    full_path += f" {discord_bot_user_id} {test_token} -c {bot_chat_channel_id}"
    full_path += f" -r {bot_test_to_run}"
    return full_path


def test_heartbeat(bash):
    """
    Wrapper method to call `test_heartbeat` method in the `discord_bot_tester.py`
    """
    assert 'CLI' in bash.run_script_inline([get_command('test_heartbeat')])


def test_this_week(bash):
    """
    Wrapper method to call `test_this_week` method in the `discord_bot_tester.py`
    """
    assert 'CLI' in bash.run_script_inline([get_command('test_this_week')])


def test_standings(bash):
    """
    Wrapper method to call `test_standings` method in the `discord_bot_tester.py`
    """
    assert 'CLI' in bash.run_script_inline([get_command('test_standings')])
