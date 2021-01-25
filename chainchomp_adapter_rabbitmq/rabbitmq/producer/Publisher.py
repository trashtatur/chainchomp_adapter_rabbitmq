import json

from chainchomplib.adapterlayer.Message import Message

from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName


class Publisher:

    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    def publish(self, message: Message):
        """
        Publishers hold the routing key to which they publish in their name.
        So the routing key can equal to the name of the publisher.
        :param message: The message to be sent
        :return: None
        """
        self.channel.basic_publish(
            exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME,
            routing_key=self.name,
            body=json.dumps(message.get_serialized())
        )
