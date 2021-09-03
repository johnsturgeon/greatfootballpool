"""Unit Test wrapper for discord_bot_tester.py"""
import os
from datetime import datetime
import pytest
from bson import ObjectId
from include.tgfp import TGFP, TGFPGame, TGFPTeam
from instance.config import get_config

config = get_config(os.getenv('FLASK_ENV'))


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
@pytest.fixture
def game(tgfp_db: TGFP) -> TGFPGame:
    return tgfp_db.games()[0]


@pytest.fixture
def west_coast_game(tgfp_db: TGFP) -> TGFPGame:
    return tgfp_db.find_games(yahoo_game_id='nfl.g.20190922025')[0]


def test_tgfpgame(game: TGFPGame):
    assert isinstance(game, TGFPGame)


def test_game_mongo_data(game):
    game_data = game.mongo_data()
    assert '_id' not in game_data
    assert 'game_status' in game_data


def test_game_save(game: TGFPGame):
    assert game.game_status == 'final'
    game.game_status = 'in progress'
    new_tgfp = TGFP()
    new_game = new_tgfp.games()[0]
    assert new_game.game_status == 'final'
    game.save()
    newer_tgfp = TGFP()
    newer_game = newer_tgfp.games()[0]
    assert newer_game.game_status == 'in progress'
    newer_game.game_status = 'final'
    newer_game.save()


# noinspection DuplicatedCode
def test_winner_id_of_game(game: TGFPGame):
    home_team_id = ObjectId('59ac8f79ee45e20848e11a88')
    road_team_id = ObjectId('59ac8d8aee45e20848e11a7c')
    assert game.winner_id_of_game == road_team_id
    game.home_team_score = 100
    assert game.winner_id_of_game == home_team_id
    game.road_team_score = 100
    assert game.winner_id_of_game is None
    game.road_team_score = 4
    assert game.winner_id_of_game == home_team_id
    game.game_status = 'in progress'
    assert game.winner_id_of_game is None


# noinspection DuplicatedCode
def test_leader_id_of_game(game: TGFPGame):
    home_team_id = ObjectId('59ac8f79ee45e20848e11a88')
    road_team_id = ObjectId('59ac8d8aee45e20848e11a7c')
    assert game.leader_id_of_game == road_team_id
    game.home_team_score = 100
    assert game.leader_id_of_game == home_team_id
    game.road_team_score = 100
    assert game.leader_id_of_game is None
    game.road_team_score = 4
    assert game.leader_id_of_game == home_team_id
    game.game_status = 'in progress'
    assert game.leader_id_of_game == home_team_id


# noinspection DuplicatedCode
def test_loser_id_of_game(game: TGFPGame):
    home_team_id = ObjectId('59ac8f79ee45e20848e11a88')
    road_team_id = ObjectId('59ac8d8aee45e20848e11a7c')
    assert game.loser_id_of_game == home_team_id
    game.home_team_score = 100
    assert game.loser_id_of_game == road_team_id
    game.road_team_score = 100
    assert game.loser_id_of_game is None
    game.road_team_score = 4
    assert game.loser_id_of_game == road_team_id
    game.game_status = 'in progress'
    assert game.loser_id_of_game is None


def test_winning_team(game: TGFPGame):
    winning_team: TGFPTeam = game.winning_team
    assert winning_team.full_name == "Kansas City Chiefs"
    game.road_team_score = 10
    game.home_team_score = 10
    assert game.winning_team is None


def test_losing_team(game: TGFPGame):
    losing_team: TGFPTeam = game.losing_team
    assert losing_team.full_name == "Jacksonville Jaguars"
    game.road_team_score = 10
    game.home_team_score = 10
    assert game.losing_team is None


def test_winning_team_score(game: TGFPGame):
    assert game.winning_team_score == 40
    game.road_team_score = 20
    assert game.winning_team_score == 26


def test_losing_team_score(game: TGFPGame):
    assert game.losing_team_score == 26
    game.road_team_score = 20
    assert game.losing_team_score == 20


def test_underdog_team_id(game: TGFPGame):
    assert game.underdog_team_id == ObjectId('59ac8f79ee45e20848e11a88')


def test_pacific_start_time(west_coast_game: TGFPGame):
    pacific_start_time: datetime = west_coast_game.pacific_start_time
    assert pacific_start_time.hour == 13
    assert pacific_start_time.minute == 25
