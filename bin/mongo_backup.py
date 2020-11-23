#!/usr/bin/python3
""" This script will back up the mongo database to a folder in the settings """
import os
import sys
import subprocess
from subprocess import check_output, CalledProcessError
from get_settings import settings
dirname = os.path.dirname(os.path.abspath(__file__))
INTERP = os.path.normpath(os.path.join(dirname, '../env/bin/python'))
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)


# TODO: Rewrite this file to use the common header
def main():
    """ Backs up the mongo db """
    mongo_settings = settings()['mongo']
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
