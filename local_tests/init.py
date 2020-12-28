"""
Load the interpreter and settings relative to this folder
"""
import common_init


def get_settings():
    """ A simple wrapper for getting the settings """
    return common_init.get_settings("../", __file__)
