HOSTNAME_RABBITMQ="_chainchomp_adapter_rabbitmq"

if ! curl -s localhost:5672 >/dev/null
then
  docker run -d --hostname "$HOSTNAME$HOSTNAME_RABBITMQ" --name "$HOSTNAME$HOSTNAME_RABBITMQ"  -p 8080:15672 -p 5672:5672 rabbitmq:3-management
fi
DOTS=''
while ! curl -s localhost:5672 >/dev/null
do
    echo -ne "Waiting for RabbitMQ $DOTS\r"
    DOTS=$DOTS'.'
  sleep 1
done
echo "RabbitMQ has started"

python -m chainchomp_adapter_rabbitmq.start