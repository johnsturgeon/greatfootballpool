"""
Drop this in any new folder to get the interpreter relative to the folder's location.

call settings = get_settings(), this will load the interpreter for your file
and return the settings
"""
import os
import sys
import json


def reload_interp(relative_interp_loc, filepath):
    """
    Reload the interpreter to the virtual environment's version.

    Return:
        returns the interpreter for the 'healthchecks' folder.
    """
    print("reloading interpreter")
    dirname = os.path.dirname(os.path.abspath(filepath))
    new_interp = os.path.normpath(os.path.join(dirname, relative_interp_loc))
    print("OLD: " + sys.executable)
    print("NEW: " + new_interp)
    if sys.executable != new_interp:
        os.execl(new_interp, new_interp, *sys.argv)


def get_settings(relative_path, filepath):
    """
    Get the settings dictionary for the current environment.

    Return:
        returns a dictionary of settings.
    """

    relative_interp_loc = relative_path + "env/bin/python"
    relative_conf_json = relative_path + "conf/settings.json"

    reload_interp(relative_interp_loc, filepath)
    dirname = os.path.dirname(os.path.abspath(filepath))
    conf_path = os.path.normpath(os.path.join(dirname, relative_conf_json))
    with open(conf_path) as config_file:
        app_settings = json.load(config_file)
    return app_settings
