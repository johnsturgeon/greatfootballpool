#!../env/bin/python
""" This script will create the launchd plist for the bot, and run it """
import plistlib
import os
import shutil
import json
from os.path import expanduser

# pylint: disable=duplicate-code
dirname = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.normpath(os.path.join(dirname, '../conf/settings.json'))
with open(conf_path) as config_file:
    settings = json.load(config_file)

os.chdir(dirname)

# initialize the variables
HOME_DIR = expanduser("~")
PLIST_FILENAME = "TGFP Discord Bot.plist"
WORKING_DIR = os.path.normpath(os.path.join(dirname, '../'))
PYTHON_BIN_PATH = os.path.normpath(os.path.join(dirname, '../env/bin/'))
LOGGING_DIR = settings['config']['log_dir']
LOG_FILE = f"{LOGGING_DIR}/discord_bot_service.launchd.log"
LAUNCHD_LIB_PATH = f"{HOME_DIR}/Library/LaunchAgents/{PLIST_FILENAME}"
PLIST_TEMPLATE_FILENAME = '../conf/discord_bot_service_template.plist'
TEMP_PLIST_FILENAME = f'../conf/{PLIST_FILENAME}'
PROGRAM_RUN_ARGUMENTS = [f'{PYTHON_BIN_PATH}/python', f'{WORKING_DIR}/bin/discord_bot_service.py']

# read the plist
with open(PLIST_TEMPLATE_FILENAME, 'rb') as f:
    pl = plistlib.load(f)

pl['StandardErrorPath'] = LOG_FILE
pl['StandardOutPath'] = LOG_FILE
pl['WorkingDirectory'] = WORKING_DIR
pl['ProgramArguments'] = PROGRAM_RUN_ARGUMENTS

# write out the new plist
with open(TEMP_PLIST_FILENAME, 'wb') as nf:
    plistlib.dump(pl, nf)

COPY_FILE = True
if os.path.exists(LAUNCHD_LIB_PATH):
    overwrite = input("LaunchAgent file exists!  Overwrite? [y/n] ")
    if overwrite.lower() != "y":
        COPY_FILE = False

if COPY_FILE:
    shutil.move(TEMP_PLIST_FILENAME, LAUNCHD_LIB_PATH)
    print(f"{TEMP_PLIST_FILENAME} moved to -> {LAUNCHD_LIB_PATH}")
else:
    os.remove(TEMP_PLIST_FILENAME)
