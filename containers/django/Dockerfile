FROM python:3.5

MAINTAINER David Calle "davidfcalle@gmail.com"

# install base dependencies
RUN apt-get install -y git

# clone the project
RUN git clone https://github.com/FixIt-App/FixIt-Server.git 

WORKDIR FixIt-Server

# install python dependencies
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "fixit.wsgi", "-D", "--error-logfile server.log"]
