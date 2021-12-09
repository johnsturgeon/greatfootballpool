SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SCRIPT_NAME="update_all"
cd $SCRIPT_PATH
cd ../flask_site
export PYTHONPATH=`pwd`
export FLASK_ENV='production'
cd ..
curl -m 10 --retry 5 https://hc-ping.com/26764645-4b82-4002-af99-48cb34b07b2f
nohup env/bin/python ${SCRIPT_PATH}/${SCRIPT_NAME}.py > logs/${SCRIPT_NAME}.out 2> logs/${SCRIPT_NAME}.err < /dev/null &