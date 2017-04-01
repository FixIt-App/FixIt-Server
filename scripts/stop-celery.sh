celery multi restart worker1 \
    -A proj \
    --logfile="../pidprofile.pid" \
    --pidfile="../celery1.log"

celery multi stopwait worker1 \
     --pidfile="../celery1.log"

