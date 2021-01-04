"""Unit Test wrapper for discord_bot_tester.py"""
from common_init import  get_settings
settings = get_settings()

# pylint: disable=wrong-import-position
import pytest  # noqa E402
from tgfp import TGFP, TGFPTeam  # noqa E402
# pylint: disable=redefined-outer-name


@pytest.fixture
def tgfp_db():
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    return TGFP(load_test_fixture=True)


# pylint: disable=missing-function-docstring
def test_team(tgfp_db):
    teams = tgfp_db.teams()
    assert len(teams) == 32
    team_1: TGFPTeam
    team_1 = teams[0]
    team_data = team_1.mongo_data()
    assert '_id' not in team_data
    assert 'short_name' in team_data
    assert team_1.wins == 4
    team_1.wins = 5
    team_1.save()
    new_data = TGFP(load_test_fixture=True)
    team_1_new = new_data.teams()[0]
    assert team_1_new.wins == 5
    team_1_new.wins = 4
    team_1_new.save()
