#!../env/bin/python
""" Unit Tests for get_settings.py """
from get_settings import settings


def test_get_settings():
    """ Checks to see if the 'get_settings' import works correctly"""
    app_settings = settings()
    assert isinstance(app_settings, dict)
    assert isinstance(app_settings['config'], dict)
    assert isinstance(app_settings['config']['debug'], bool)
