import pika
from pika.adapters.blocking_connection import BlockingConnection


class RabbitMQConnector:

    LOCAL_RABBITMQ_ADDRESS = 'localhost'

    @staticmethod
    def connect(address=LOCAL_RABBITMQ_ADDRESS) -> BlockingConnection:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=address))
        return connection
