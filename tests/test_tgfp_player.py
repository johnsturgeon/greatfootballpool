"""Unit Test wrapper for discord_bot_tester.py"""
import math
import pytest
from include.tgfp import TGFP, TGFPPick, TGFPPlayer


# pylint: disable=redefined-outer-name
@pytest.fixture
def tgfp_db():
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    return TGFP()


@pytest.fixture
def tgfp_db_reg_season_in_pregame(tgfp_db):
    """
    Extends the :func:`tgfp_db_reg_season` database method, sets one game in the final week to
    'pregame'

    :param tgfp_db: Test DB with all the regular season games loaded
    :type tgfp_db: TGFP
    :return: Same DB as input with one game set to 'pregame'
    :rtype: TGFP
    """
    last_game = tgfp_db.find_games(ordered_by='week_no')[-1]
    last_game.game_status = 'pregame'
    return tgfp_db


# pylint: disable=missing-function-docstring
@pytest.fixture()
def player(tgfp_db):
    players = tgfp_db.players()
    return players[0]


@pytest.fixture()
def player_inactive(tgfp_db: TGFP):
    return tgfp_db.find_players(player_email='jamesvanboxtel@gmail.com')[0]


def test_player(tgfp_db):
    players = tgfp_db.players()
    assert len(players) == 27
    assert isinstance(players[0], TGFPPlayer)


def test_player_wins(player):
    assert player.wins() == 166
    assert player.wins(week_no=2) == 10
    assert player.wins(week_through=2) == 21


def test_player_win_csv(player: TGFPPlayer):
    csv = player.win_csv()
    assert ',' in csv
    split_csv = csv.split(',')
    # check that the number of fields equal the number of weeks that there are picks
    week_number = 0
    final_week_total = 0
    for week_total in split_csv:
        if week_total != 'John':
            int_week_total = int(week_total)
            week_number += 1
            assert int_week_total == player.wins(week_through=week_number) +\
                   player.bonus(week_through=week_number)
            final_week_total = int_week_total
    assert final_week_total == player.wins() + player.bonus()


def test_player_losses(player):
    assert player.losses() == 101
    assert player.losses(week_no=2) == 6


def test_player_bonus(player):
    assert player.bonus() == 21
    assert player.bonus(week_no=1) == 2
    assert player.bonus(week_through=6) == 11


def test_player_last_things(player: TGFPPlayer):
    assert player.last_bonus() == -1
    assert player.last_wins() == 0
    assert player.last_losses() == 1


def test_player_total_points(player: TGFPPlayer):
    assert player.total_points() == player.wins() + player.bonus()


def test_player_name(player: TGFPPlayer):
    assert player.full_name() == "John Sturgeon"


def test_player_winning_pct(player: TGFPPlayer, player_inactive: TGFPPlayer):
    total_games = player.wins() + player.losses()
    win_percent = player.wins() / total_games
    assert math.isclose(win_percent, player.winning_pct(), abs_tol=0.00001)
    assert player_inactive.winning_pct() == 0


def test_player_this_weeks_picks(
        tgfp_db_reg_season_in_pregame: TGFP,
        player: TGFPPlayer,
        player_inactive: TGFPPlayer
):
    this_weeks_pick = player.this_weeks_picks()
    assert isinstance(this_weeks_pick, TGFPPick)
    assert player_inactive.this_weeks_picks() is None
    this_weeks_picks: TGFPPick
    this_weeks_picks = player.this_weeks_picks()
    assert this_weeks_picks.week_no == tgfp_db_reg_season_in_pregame.current_week()


def test_player_mongo_data(player: TGFPPlayer):
    player_data = player.mongo_data()
    assert '_id' not in player_data
    assert 'last_name' in player_data


def test_player_save(player: TGFPPlayer):
    assert player.first_name == "John"
    player.first_name = "Juan"
    player.save()
    new_data = TGFP()
    new_player = new_data.players()[0]
    assert new_player.first_name == "Juan"
    new_player.first_name = "John"
    new_player.save()
