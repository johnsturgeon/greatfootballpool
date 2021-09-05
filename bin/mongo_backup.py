""" This script will back up the mongo database to a folder in the settings """
import os
import subprocess
from subprocess import check_output, CalledProcessError

# pylint: disable=import-error
from instance.config import get_config

config = get_config(os.getenv('FLASK_ENV'))


def main():
    """ Backs up the mongo db """
    try:
        output = check_output([
            '/usr/local/bin/mongodump',
            '-h', config.MONGO_HOST,
            '-u', config.MONGO_USERNAME,
            '-p', config.MONGO_PASSWORD,
            f'--authenticationDatabase={config.MONGO_DB}',
            '-d', config.MONGO_DB,
            '-o', config.MONGO_BACKUP_FOLDER
        ], stderr=subprocess.STDOUT).decode("utf-8")
    except CalledProcessError as err:
        raise RuntimeError('Could not back up Mongo DB') from err

    if 'done dumping' not in output:
        raise RuntimeError('Mongo DB not backed up')


if __name__ == "__main__":
    main()
