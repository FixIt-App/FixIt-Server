FROM python:3.5

MAINTAINER David Calle "davidfcalle@gmail.com"

# install base dependencies
RUN apt-get install -y git

# clone the project
RUN git clone https://github.com/FixIt-App/FixIt-Server.git 

WORKDIR FixIt-Server

# install python dependencies
RUN pip install -r requirements.txt

CMD CMD ["celery", "multi", "start", "worker1", "-A", "fixit", "--pidfile=\"../pidprofile.pid\"", "--logfile=\"../celery1.log\""]
