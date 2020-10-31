#!/bin/bash

cd "$(dirname "$0")" || exit
BASEDIR=$(pwd -P)
DOT_ENV="${BASEDIR}/../conf/.env"
if [[ ! -e $DOT_ENV ]] ; then
	echo "Can't find the .env file: ${DOT_ENV}"
fi
# shellcheck disable=SC2046
export $(grep -Ev '^#' "${DOT_ENV}" | xargs)

/usr/local/bin/mongodump -u admin -p "${MONGO_ADMIN_PASSWORD}" --authenticationDatabase=admin -d tgfp -o "${MONGO_DUMP_FOLDER}"
