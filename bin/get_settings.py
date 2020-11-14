#!../env/bin/python
""" This script will back up the mongo database to a folder in the settings """
import os
import json


def settings():
    """
    Returns the current 'settings.json' file in the settings dictionary
    Returns:
      settings: dict
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(dirname, '../conf/settings.json'))
    with open(conf_path) as config_file:
        app_settings = json.load(config_file)
    return app_settings
