import init

settings = init.get_settings()

# pylint: disable=wrong-import-position
import pytest
from pytest import FixtureRequest
from tgfp import TGFP, TGFPPick
from bson import ObjectId
# pylint: disable=redefined-outer-name


@pytest.fixture
def tgfp_db() -> TGFP:
    """
    This will return the default tgfp database object loaded with the test fixture

    :return: tgfp database object
    :rtype: TGFP
    """
    return TGFP(load_test_fixture=True)


@pytest.fixture
def pick(tgfp_db, request: FixtureRequest) -> TGFPPick:
    pick: TGFPPick = tgfp_db.picks()[0]

    def reset_db():
        pick.load_record()
        pick.save()

    request.addfinalizer(reset_db)
    return pick


def test_pick(pick: TGFPPick):
    assert len(pick.pick_detail) == 16


def test_pick_init():
    new_pick = TGFPPick(TGFP(load_test_fixture=True), data=None)
    assert hasattr(new_pick, 'week_no') is False


def test_winner_for_game_id(pick):
    assert pick.winner_for_game_id(ObjectId('5d6fcc5fd4fa6803c6505831')) == ObjectId('59ac8d38ee45e20848e11a6b')
    assert pick.winner_for_game_id(ObjectId('5d827532dd2d55018d8d756b')) is None


def test_save(pick):
    assert pick.wins == 11
    pick.wins = 4
    pick.save()
    new_pick: TGFPPick = TGFP(load_test_fixture=True).picks()[0]
    assert new_pick.id == pick.id
    assert new_pick.wins == 4


def test_load_record(pick):
    assert pick.wins == 11
    pick.wins = 3
    assert pick.wins == 3
    pick.load_record()
    assert pick.wins == 11
