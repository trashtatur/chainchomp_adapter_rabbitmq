from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Publisher import Publisher


class Producer:

    def __init__(self, connection: BlockingConnection):
        self.publishers = {}
        self.channel = connection.channel()

    def create_new_publisher(self, name) -> Publisher:
        self.channel.exchange_declare(exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME, exchange_type='direct')
        resulted_queue = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = resulted_queue.method.queue
        self.channel.queue_bind(
            exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME,
            queue=queue_name,
            routing_key=name
        )
        publisher = Publisher(name, self.channel)
        self.publishers[name] = publisher
        return publisher
