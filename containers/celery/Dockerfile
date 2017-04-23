FROM python:3.5

MAINTAINER David Calle "davidfcalle@gmail.com"

# install base dependencies
RUN apt-get install -y git

# clone the project
ADD . .

# install python dependencies
RUN pip install -r requirements.txt

CMD ["celery", "-A", "fixit", "worker", "--loglevel=info"]
