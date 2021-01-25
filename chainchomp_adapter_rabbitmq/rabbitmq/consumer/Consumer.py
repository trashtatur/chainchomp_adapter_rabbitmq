from pika.adapters.blocking_connection import BlockingConnection

from chainchomp_adapter_rabbitmq.messaging.IncomingMessageHandler import IncomingMessageHandler
from chainchomp_adapter_rabbitmq.rabbitmq import RabbitMQExchangeName
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Subscriber import Subscriber
from chainchomp_adapter_rabbitmq.socket.SocketEmitter import SocketEmitter


class Consumer:

    def __init__(self, socket_emitter: SocketEmitter):
        self.subscribers = {}
        self.socket_emitter = socket_emitter

    def create_new_subscriber(self, connection: BlockingConnection, name: str) -> Subscriber:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME,
            exchange_type='direct',
            durable=True
        )
        resulted_queue = channel.queue_declare(queue='', exclusive=True, durable=True)
        queue_name = resulted_queue.method.queue
        channel.queue_bind(exchange=RabbitMQExchangeName.RABBITMQ_EXCHANGE_NAME, queue=queue_name, routing_key=name)
        subscriber = Subscriber(channel, name, queue_name, IncomingMessageHandler(self.socket_emitter))
        self.subscribers[name] = subscriber
        return subscriber
