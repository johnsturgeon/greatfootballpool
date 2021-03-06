"""Discord bot runs in the background and handles all requests to discord."""
from common_init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
import urllib.request  # noqa: E402
import socket  # noqa: E402
import sentry_sdk  # noqa: E402
from sentry_sdk import capture_exception, capture_message  # noqa: E402
SENTRY_DSN = settings['config']['sentry_dsn']
ENVIRONMENT = settings['config']['environment']
FLASK_SITE_URL = settings['config']['login_url']
WEB_CHECK_URL = settings['healthchecks']['tgfp_web_check_url']
sentry_sdk.init(dsn=SENTRY_DSN, environment=ENVIRONMENT)

try:
    RETURN_CODE = urllib.request.urlopen(FLASK_SITE_URL).getcode()
except socket.error:
    RETURN_CODE = 404

if RETURN_CODE == 200:
    try:
        urllib.request.urlopen(WEB_CHECK_URL, timeout=10)
    except socket.error as exception:
        capture_exception(exception)
else:
    capture_message("TGFP Web Site is DOWN")
