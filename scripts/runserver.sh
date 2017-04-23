python3 manage.py migrate
gunicorn -w 4 -b 0.0.0.0:8000 fixit.wsgi