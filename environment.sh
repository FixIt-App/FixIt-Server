# environment variables for rabbitmq server
export RABBITMQ_HOST=
export RABBITMQ_PORT=
export RABBITMQ_DEFAULT_USER=
export RABBITMQ_DEFAULT_PASS=
export RABBITMQ_DEFAULT_VHOST=
export BROKER_URL="amqp://$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS@$RABBITMQ_HOST:$RABBITMQ_PORT/$RABBITMQ_DEFAULT_VHOST"


# environment variables for postgres server
export POSTGRES_DATABASE=
export POSTGRES_USER=
export POSTGRES_PASSWORD=
export POSTGRES_HOST=

# email configuration
export EMAIL_API_KEY=

# aws configuration
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=

#firebase configuration
export FIREBASE_CUSTOMER_KEY=

# server conf
export DNS_NAME=localhost
