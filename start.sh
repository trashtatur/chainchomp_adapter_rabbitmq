HOSTNAME_RABBITMQ="_chainchomp_adapter_rabbitmq"

docker run -d --hostname "$HOSTNAME$HOSTNAME_RABBITMQ" --name "$HOSTNAME$HOSTNAME_RABBITMQ"  -p 8080:15672 -p 5672:5672 rabbitmq:3-management
RESULT=$( docker inspect -f {{.State.Running}} "$HOSTNAME$HOSTNAME_RABBITMQ")

DOTS=''
while ! curl -s localhost:5672 >/dev/null
do
    echo -ne "Waiting for RabbitMQ $DOTS\r"
    DOTS=$DOTS'.'
  sleep 1
done
echo "RabbitMQ has started"

python ./chainchomp_adapter_rabbitmq/rabbitmq/RabbitMQConnector.py