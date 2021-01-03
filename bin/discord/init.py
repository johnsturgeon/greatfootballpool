"""
Load the interpreter and settings relative to this folder
"""
import common_init


def get_settings():
    """ Wrapper method for getting the settings """
    return common_init.get_settings("../../", __file__)
