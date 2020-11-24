#!/bin/bash
BASEDIR=$(dirname "$0")
cd "$BASEDIR/../" || exit
python3 -m venv env
# shellcheck disable=SC1091
source env/bin/activate
pip install --use-feature=2020-resolver --upgrade pip
pip install --use-feature=2020-resolver -r requirements.txt
cp conf/tgfp_paths.pth env/lib/python3.*/site-packages
# Create conf/.env file
# .env
should_create_env="N"
if [[ ! -e conf/.env ]] ; then
	should_create_env="Y"
else
	echo -n "Re-create the .env file? [y/n]"
	read -r do_dotenv
	if [[ ${do_dotenv} == "Y" || ${do_dotenv} == "y" ]]	 ; then
		should_create_env="Y"
	fi
fi

if [[ $should_create_env == "Y" ]] ; then
	echo "---"
	echo "Creating the .env file"
	echo "---"
	echo "Enter the configuration values after the prompt; quotes will be added"
	echo ""
	touch conf/.env
	cat /dev/null > conf/.env
	IFS='
	'
	for conf_var_line in $(dotenv -f conf/template.env list) ; do
		conf_var=$(echo "${conf_var_line}" | awk -F= '{print $1}')
		echo -n "${conf_var}="
		read -r conf_var_result
		echo "Writing value to .env file"
		dotenv -f conf/.env -q always set "${conf_var}" "${conf_var_result}"
	done
fi
export "$(dotenv -f conf/.env get LOGGING_DIR)"
if [[ ! -d $LOGGING_DIR ]] ; then
	mkdir "$LOGGING_DIR"
fi

uname_out="$(uname -s)"
case "${uname_out}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=macOS;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${uname_out}"
esac
if [[ ${machine} == "macOS" ]] ; then
	echo ""
	echo "You're running on macOS.  Would you like to install a launchd daemon for the football pool bot?"
	echo -n "[y/n]:"
	read -r install_launchd
	if [[ ${install_launchd} == "Y" || ${install_launchd} == "y" ]]	 ; then
		env/bin/python bin/create_bot_launchd.py
		echo "Bot Service Status:"
		bin/discord_bot_service.sh status
	fi
fi
echo -n ""
deactivate
