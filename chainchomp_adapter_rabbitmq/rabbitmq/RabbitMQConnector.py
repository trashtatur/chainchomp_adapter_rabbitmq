import pika
from pika import BlockingConnection


class RabbitMQConnector:

    @staticmethod
    def connect_to_rabbit_mq_instance() -> BlockingConnection:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        return connection
