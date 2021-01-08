from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Subscriber import Subscriber


class Consumer:

    def __init__(self):
        self.subscribers = {}

    def create_new_subscriber(self, connection: BlockingConnection, name: str) -> Subscriber:
        channel = connection.channel()
        resulted_queue = channel.queue_declare(queue='', exclusive=True)
        queue_name = resulted_queue.method.queue
        channel.queue_bind(exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME, queue=queue_name, routing_key=name)
        subscriber = Subscriber(channel, name, queue_name)
        self.subscribers[name] = subscriber
        return subscriber
