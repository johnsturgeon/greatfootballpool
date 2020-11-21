#!/usr/bin/python
"""Discord bot runs in the background and handles all requests to discord."""
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
import os  # noqa: E402
import socket  # noqa: E402
import urllib.request  # noqa: E402
import sentry_sdk  # noqa: E402
from sentry_sdk import capture_exception, capture_message  # noqa: E402

SENTRY_DSN = settings['config']['sentry_dsn']
ENVIRONMENT = settings['config']['environment']
BOT_CHECK_URL = settings['healthchecks']['discord_bot_check_url']
sentry_sdk.init(dsn=SENTRY_DSN, environment=ENVIRONMENT)
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
