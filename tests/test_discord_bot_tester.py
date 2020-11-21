#!/usr/bin/env python
"""Unit Test wrapper for discord_bot_tester.py"""
import os
import init
settings = init.get_settings()


def get_command(bot_test_to_run="all"):
    dirname = os.path.dirname(os.path.abspath(__file__))
    fullpath = f"{dirname}/discord_bot_tester.py"
    fullpath += " 753299507130663149 Nzc5MzgzODU4MDk2MjQyNzE4.X7fvyA.rj4O0LJP79xv3LjAPOJHP8SLDyA -c 753985973708390523"
    fullpath += f" -r {bot_test_to_run}"
    return fullpath


def test_hearbeat(bash):
    assert 'CLI' in bash.run_script_inline([get_command('test_heartbeat')])


def test_this_week(bash):
    assert 'CLI' in bash.run_script_inline([get_command('test_this_week')])


def test_standings(bash):
    assert 'CLI' in bash.run_script_inline([get_command('test_standings')])
