# environment variables for rabbitmq server
export RABBITMQ_DEFAULT_USER=fixit
export RABBITMQ_DEFAULT_PASS=
export RABBITMQ_DEFAULT_VHOST=fixit
export BROKER_URL="amqp://$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS@localhost:5672//$RABBITMQ_DEFAULT_VHOST"


# environment variables for postgres server
export POSTGRES_USER=fixit
export POSTGRES_PASSWORD=

# django configurations
export MEDIA_ROOT=

# email configuration
export EMAIL_API_KEY=

# aws configuration
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

