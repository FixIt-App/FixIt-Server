  # install & run ssh-agent
apt-get -qq update -y
apt-get -qq install openssh-client -y
  # setup the private key
eval $(ssh-agent -s)
ssh-add <(echo "$ALPHA_SSH_KEY")
mkdir -p ~/.ssh
echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
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

git pull origin develop

source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate

# start gunicorn, only two workers for now
gunicorn -w 15 -b 0.0.0.0:8000 fixit.wsgi -D --error-logfile server.log

# start celery
celery multi start worker1 -A fixit --pidfile="../pidprofile.pid" \ --logfile="../celery1.log"
