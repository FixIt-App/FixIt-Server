docker run --name postgres \
           -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
           -e POSTGRES_USER=$POSTGRES_USER \
           -p 5432:5432 \
           -d postgres:9.6
