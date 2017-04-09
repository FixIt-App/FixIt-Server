docker run  -d -p 49001:8080 \
            -v $PWD/jenkins:/var/jenkins_home \
            -t jenkins