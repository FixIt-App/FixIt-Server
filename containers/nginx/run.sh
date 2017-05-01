docker run  --name nginx --add-host=docker:$DNS_NAME -p 80:80 -p 443:443 -d nginx
