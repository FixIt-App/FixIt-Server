celery multi restart worker1 \
    -A fixit \
    --logfile="../pidprofile.pid" \
    --pidfile="../celery1.log"

celery multi stopwait worker1 \
     --pidfile="../celery1.log"
# TODO: create pidprofile.pid file with date
rm ../pidprofile.pid
