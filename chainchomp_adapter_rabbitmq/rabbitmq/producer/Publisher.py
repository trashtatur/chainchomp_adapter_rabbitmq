from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName


class Publisher:

    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    def publish(self, message, key):
        self.channel.basic_publish(
            exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME,
            routing_key=key,
            body=message
        )
