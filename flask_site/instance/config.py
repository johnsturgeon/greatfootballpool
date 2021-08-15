""" Configuration file """
from logging.handlers import RotatingFileHandler
import logging
import os


# pylint: disable=missing-class-docstring
class InvalidEnvironment(Exception):
    pass


# pylint: disable=too-few-public-methods
class Config:
    """ Base configuration class """
    TESTING = False

    APEX_LEGENDS_API_KEY = "if1gmS2sksadwheeExjL"

    DISCORD_CLIENT_ID = "851575510039003179"
    DISCORD_CLIENT_SECRET = "Qd80hm_BMhNQjFfc7XRBaIH5A3gbYSut"

    MONGO_HOST = "208.113.129.246"
    MONGO_DB = "apex_legends"
    MONGO_USERNAME = "apex_admin"
    MONGO_PASSWORD = "6KbzNU3@jntf7"
    ONLINE_CHECK_INTERVAL = 60
    STRYDER_URL = "https://r5-crossplay.r5prod.stryder.respawn.com/user.php"
    LOG_LEVEL = "INFO"
    DISCORD_BOT_CHANNEL_ID = 754017265044684921
    DISCORD_GUILD = "The Great Football Pool"
    DISCORD_WEBHOOK_BOT_ID = 756899747276652594
    DISCORD_ADMIN_EMAIL = "greatfootballpool@icloud.com"

    def logger(self, name: str) -> logging.Logger:
        """ Return the common logger """
        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, self.LOG_LEVEL))
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path += '/../../logs/apex_logger.log'
        handler = RotatingFileHandler(file_path, maxBytes=1000000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


class ProductionConfig(Config):
    """ Configuration for production instances """

    DISCORD_TOKEN = "NzUzMjk5NTA3MTMwNjYzMTQ5.X1kK1g.80-We5mF1GPQnGjfsv-_gSJZmXk"

    SECRET_KEY = "55f1fa49-ee7e-4268-80ba-e93ec3394cea"
    LOG_LEVEL = "ERROR"
    LOG_COLLECTION = "log"
    OAUTHLIB_INSECURE_TRANSPORT = "false"
    DISCORD_REDIRECT_URI = "https://apex.goshdarnedhero.com/callback"


class DevelopmentConfig(Config):
    """ Configuration for development instance """

    DISCORD_TOKEN = "Nzc5MzgzODU4MDk2MjQyNzE4.X7fvyA.qjHYao5rJWNZ7w7rbz6J0rQjVH8"

    SECRET_KEY = "28bc0401-0eae-4623-bbc1-8ddea071e2f1"
    LOG_LEVEL = "DEBUG"
    LOG_COLLECTION = "dev_log"
    OAUTHLIB_INSECURE_TRANSPORT = "true"
    DISCORD_REDIRECT_URI = "http://127.0.0.1:5000/callback"


class TestConfig(ProductionConfig):
    """ Test Configuration """

    TESTING = True
    LOG_LEVEL = "WARN"
    MONGO_DB = "test_apex"
    MONGO_USERNAME = "test_apex_admin"
    MONGO_PASSWORD = "@ZPCuiPbBGoxv6XWzue*7DVe"


def get_config(environment: str):
    """ Factory method for returning the correct config"""
    if environment.upper() == 'PRODUCTION':
        return ProductionConfig()
    if environment.upper() == 'DEVELOPMENT':
        return DevelopmentConfig()
    if environment.upper() == 'TEST':
        return TestConfig()
    raise InvalidEnvironment


# {
#     "mongo": {
#         "backup_folder": "/Users/johnsturgeon/Dropbox/Documents/tgfp_backups",
#         "admin_password": "UfJ7NPmH9WRf",
#         "db_url": "mongodb://tgfp:4P5q5wRmSyKt@johnsturgeon.dynu.net:27017/tgfp",
#         "test_db_url": "mongodb://tgfp:4P5q5wRmSyKt@johnsturgeon.dynu.net:27017/tgfp_test"
#     },
#     "config": {
#         "sentry_dsn": "https://24c31c9cd15042a0982df8c71733381a@o48973.ingest.sentry.io/104811",
#         "flask_app_secret_key": "6a6c7365-1059-46b9-9ceb-4dea594e1d03",
#         "debug": false,
#         "log_dir": "/Users/johnsturgeon/Code/tgfp_bot/logs",
#         "environment": "production",
#         "login_url": "https://greatfootballpool.com/login"
#     },
#     "discord": {
#         "webhook_bot_id": ,
#         "discord_bot_user_id": 753299507130663149,
#         "test_bot_user_id": 779383858096242718,
#         "bot_chat_channel_id": ,
#         "guild": "",
#         "admin_email": "john.sturgeon@gmail.com"
#     },
#     "healthchecks": {
#         "discord_bot_check_url": "https://hc-ping.com/093cbb45-7a55-432f-8a50-6ae4ec474e4f",
#         "tgfp_web_check_url": "https://hc-ping.com/2ef3cf78-b4a8-46b2-9470-94b61e012957"
#     }
# }
