#!/usr/bin/env python
""" This script will back up the mongo database to a folder in the settings """
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
import launchctl  # noqa: E402


def restart():
    launchctl.stop('TGFP: Discord Bot')
