#!../env/bin/python
""" Discord bot runs in the background and handles all requests to discord """
import os
import urllib.request
import socket
import json
import sentry_sdk
from sentry_sdk import add_breadcrumb, capture_exception, capture_message

dirname = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.normpath(os.path.join(dirname, '../conf/settings.json'))
with open(conf_path) as config_file:
    settings = json.load(config_file)

SENTRY_DSN = settings['config']['sentry_dsn']
ENVIRONMENT = settings['config']['environment']
BOT_CHECK_URL = settings['healthchecks']['discord_bot_check_url']
sentry_sdk.init(dsn=SENTRY_DSN, environment=ENVIRONMENT)
add_breadcrumb(
    category='config',
    message=f'Configuration file: {conf_path}',
    level='debug',
)
stream = os.popen('pgrep -f discord_bot_service.py', mode='r')
pid = stream.read()
pid_str = pid.rstrip()
if pid_str.isnumeric():
    try:
        urllib.request.urlopen(BOT_CHECK_URL, timeout=10)
    except socket.error as exception:
        capture_exception(exception)
else:
    capture_message("Discord Bot Service is DOWN")
