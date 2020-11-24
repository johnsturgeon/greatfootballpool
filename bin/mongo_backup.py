#!/usr/bin/env python
""" This script will back up the mongo database to a folder in the settings """
from init import get_settings
settings = get_settings()
# pylint: disable=wrong-import-position
# pylint: disable=C0411
import subprocess  # noqa: E402
from subprocess import check_output, CalledProcessError  # noqa: E402


def main():
    """ Backs up the mongo db """
    mongo_settings = settings['mongo']
    dump_folder = mongo_settings['backup_folder']
    admin_passwd = mongo_settings['admin_password']
    try:
        output = check_output(['/usr/local/bin/mongodump', '-u', 'admin',
                               '-p', admin_passwd, '--authenticationDatabase=admin', '-d', 'tgfp',
                               '-o', dump_folder
                               ], stderr=subprocess.STDOUT).decode("utf-8")
    except CalledProcessError as err:
        raise RuntimeError('Could not back up Mongo DB') from err

    if 'done dumping' not in output:
        raise RuntimeError('Mongo DB not backed up')


if __name__ == "__main__":
    main()
