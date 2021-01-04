""" Unit Tests for mongo_backup.py """
import mongo_backup
import pytest


def test_main(mocker):
    """This is just a test for nothing"""
    try:
        mongo_backup.main()
    except RuntimeError:
        assert False
    assert True

    settings = {
                'mongo': {
                    'backup_folder': '/tmp',
                    'admin_password': 'bad_password'
                }
            }
    mocker.patch.object(mongo_backup, 'settings', return_value=settings)
    with pytest.raises(RuntimeError):
        mongo_backup.main()
