"""
call settings = get_settings(),this will load the settings
"""
import os
import json


def get_settings():
    """
    Get the settings for the current environment

    Return:
        returns a dictionary of settings.
    """

    relative_conf_json = '../conf/settings.json'

    dirname = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(dirname, relative_conf_json))
    with open(conf_path) as config_file:
        app_settings = json.load(config_file)
    return app_settings
