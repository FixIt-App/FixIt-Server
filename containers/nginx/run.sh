hostip=35.166.206.134
docker run  --name nginx --add-host=docker:$hostip -p 80:80 -d nginx
