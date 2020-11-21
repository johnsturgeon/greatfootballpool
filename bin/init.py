"""
Drop this in any new folder to get the interpreter relative to the folder's location.

call settings = get_settings(), this will load the interpreter for your file
and return the settings
"""
import os
import sys
import json

RELATIVE_INTERP_LOC = "../env/bin/python"
RELATIVE_CONF_JSON = "../conf/settings.json"


def reload_interp():
    """
    Reload the interpreter to the virtual environment's version.

    Return:
        returns the interpreter for the 'healthchecks' folder.
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    new_interp = os.path.normpath(os.path.join(dirname, RELATIVE_INTERP_LOC))
    if sys.executable != new_interp:
        os.execl(new_interp, new_interp, *sys.argv)


def get_settings():
    """
    Get the settings dictionary for the current environment.

    Return:
        returns a dictionary of settings.
    """
    reload_interp()
    dirname = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(dirname, RELATIVE_CONF_JSON))
    with open(conf_path) as config_file:
        app_settings = json.load(config_file)
    return app_settings
