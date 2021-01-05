from chainchomp_adapter_rabbitmq.rabbitmq.RabbitMQConnector import RabbitMQConnector
from chainchomp_adapter_rabbitmq.socket import SocketClient

RabbitMQConnector.connect_to_rabbit_mq_instance()
SocketClient.connect()
