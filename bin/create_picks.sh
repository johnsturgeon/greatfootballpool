SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SCRIPT_NAME="create_picks"
cd $SCRIPT_PATH
cd ../flask_site
export PYTHONPATH=`pwd`
export FLASK_ENV='production'
cd ..
curl -m 10 --retry 5 https://hc-ping.com/ae09aed7-ec22-47f6-9e1a-67ab5421aec3
nohup env/bin/python ${SCRIPT_PATH}/${SCRIPT_NAME}.py > logs/${SCRIPT_NAME}.out 2> logs/${SCRIPT_NAME}.err < /dev/null &