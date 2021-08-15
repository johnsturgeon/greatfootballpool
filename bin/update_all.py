"""This is a 'do everything' script for updating the scores in mongo."""
from common_init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
from update_scores import main as update_scores  # noqa E402
from mongo_backup import main as backup_db  # noqa E402
from update_win_loss import main as update_win_loss  # noqa E402


def main():
    """Execute the steps in order necessary to update everything"""
    backup_db()
    update_scores()
    update_win_loss()
    restart()


if __name__ == "__main__":
    main()
