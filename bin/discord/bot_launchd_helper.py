#!/usr/bin/env python
""" This script will back up the mongo database to a folder in the settings """
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
import subprocess  # noqa E402


def restart():
    try:
        subprocess.call(
            [
                '/bin/launchctl',
                'unload',
                '-w',
                '/Users/johnsturgeon//Library/LaunchAgents/TGFP Discord Bot.plist'
            ]
        )
        subprocess.call(
            [
                '/bin/launchctl',
                'load',
                '-w',
                '/Users/johnsturgeon//Library/LaunchAgents/TGFP Discord Bot.plist'
            ]
        )
    except subprocess.CalledProcessError as err:
        raise RuntimeError('Could not stop TGFP: Discord Bot') from err
