"""Unit Test TGFP Team """
import pytest
from include.tgfp import TGFP, TGFPTeam


# pylint: disable=redefined-outer-name
@pytest.fixture
def tgfp_db():
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    return TGFP()


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
    new_data = TGFP()
    team_1_new = new_data.teams()[0]
    assert team_1_new.wins == 5
    team_1_new.wins = 4
    team_1_new.save()
