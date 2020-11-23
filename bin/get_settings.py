""" This module will back up the mongo database to a folder in the settings """
import os
import json
import warnings
# TODO: Deprecate this file


def settings():
    """
    Returns the current 'settings.json' file in the settings dictionary
    Returns:
      settings: dict
    """
    warnings.warn("This method is deprecated", DeprecationWarning)
    dirname = os.path.dirname(os.path.abspath(__file__))
    print(dirname)
    conf_path = os.path.normpath(os.path.join(dirname, '../conf/settings.json'))
    with open(conf_path) as config_file:
        app_settings = json.load(config_file)
    return app_settings
