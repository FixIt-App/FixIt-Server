ssh -t root@104.131.151.33
# stop all processes
pkill python3
pkill celery
pkill gunicorn

docker restart postgres
docker restart rabbitmq-instance1

# TODO: save old logging files
rm pidprofile.pid celery1.log

# pulling changes, and updating static files
cd FixIt-Server
git pull origin develop

source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate

# start gunicorn, only two workers for now
gunicorn -w 2 -b 0.0.0.0:8000 fixit.wsgi -D --error-logfile server.log

# start celery
celery multi start worker1 -A fixit --pidfile="../pidprofile.pid" \ --logfile="../celery1.log"
