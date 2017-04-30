# stop all processes
pkill python3
pkill celery
pkill gunicorn

# TODO: save old logging files
rm pidprofile.pid celery1.log

# pulling changes, and updating static files
cd FixIt-Server
git pull origin develop

source fixit.env
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate

# start gunicorn, only two workers for now
gunicorn -w 2 -b 0.0.0.0:8080 fixit.wsgi -D --error-logfile server.log

# start celery
celery multi start worker1 -A fixit --pidfile="../pidprofile.pid" --logfile="../celery1.log"
