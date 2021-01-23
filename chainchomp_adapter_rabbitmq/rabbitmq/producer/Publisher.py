import json

from chainchomplib.adapterlayer.Message import Message

from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName


class Publisher:

    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    def publish(self, message: Message, key):
        self.channel.basic_publish(
            exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME,
            routing_key=key,
            body=json.dumps(message.get_serialized())
        )
