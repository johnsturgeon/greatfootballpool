#!/usr/bin/env python
"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""
import sys
import init
settings = init.get_settings()

# pylint: disable=wrong-import-position
from distest import TestCollector  # noqa E402
from distest import run_dtest_bot  # noqa E402

# The tests themselves
test_collector = TestCollector()


@test_collector()
async def test_this_week(interface):
    await interface.assert_reply_contains("!TGFP This Week", "Results for")


@test_collector()
async def test_standings(interface):
    await interface.assert_reply_contains("!TGFP Standings", "Name  |  W  |  L  |Bonus| GB")


@test_collector()
async def test_heartbeat(interface):
    await interface.assert_reply_contains("!TGFP Test", "💗")


if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
