from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel

from chainchomp_adapter_rabbitmq.rabbitmq.RabbitMQConnector import RabbitMQConnector
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Consumer import Consumer
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Producer import Producer


class ChainfileHandler:

    @staticmethod
    def handle_incoming_local_chainfile(chainfile_model: ChainfileModel, consumer: Consumer, producer: Producer):
        for previous_link in chainfile_model.previous_links:
            name_and_ip = previous_link.split('::')
            connection = RabbitMQConnector.connect_to_rabbit_mq_instance(name_and_ip[0])
            subscriber = consumer.create_new_subscriber(connection, chainfile_model.chainlink_name)
            subscriber.start_subscriber()

        for next_link in chainfile_model.next_links:
            name_and_ip = next_link.split('::')
            producer.create_new_publisher(name_and_ip[1])

    @staticmethod
    def handle_incoming_remote_chainfile(chainfile_model: ChainfileModel):
        pass