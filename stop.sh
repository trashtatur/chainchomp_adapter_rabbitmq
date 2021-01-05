HOSTNAME_RABBITMQ="_chainchomp_adapter_rabbitmq"
docker stop "$HOSTNAME$HOSTNAME_RABBITMQ" || true
docker rm "$HOSTNAME$HOSTNAME_RABBITMQ" || true
