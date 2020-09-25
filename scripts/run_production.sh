#!/bin/bash
export FLASK_APP=home_fserver && export FLASK_ENV=production
cd $HOME/home_fserver && source $HOME/home_fserver/venv/bin/activate
UWSGI_UID=$( whoami ) nohup uwsgi --ini home_fserver.ini > ./instance/server.out 2>&1 &
sudo chown $( whoami ):www-data /tmp/home_fserver.sock
sleep 1
grep -E "master.*pid" ./instance/server.out > ./instance/master_pid.txt

