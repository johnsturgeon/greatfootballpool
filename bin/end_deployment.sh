#!/bin/bash
###
# This script will put the site in maintenance mode, stop the DB scraper
###
SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
sudo supervisorctl restart greatfootballpool
rm $SCRIPT_PATH/../maintenance
