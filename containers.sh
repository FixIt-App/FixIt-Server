mkdir -p deploy deploy_tmp
cp -r * deploy && cp -r * deploy_tmp
cd deploy
cp -r ../deploy_tmp/ celery/fixit && cp -r ../deploy_tmp/ django/fixit
cd containers
docker-compose build
docker-compose up -d
rm -rf deploy_tmp