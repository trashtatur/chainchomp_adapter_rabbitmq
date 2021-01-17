from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.data.RemoteChainfileDTO import RemoteChainfileDTO

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
    def handle_incoming_remote_chainfile(
            remote_chainfile_dto: RemoteChainfileDTO,
            consumer: Consumer,
            producer: Producer
    ):
        """
        This interprets an incoming remote chainfile and prepares the adapter for anything related to that
        Only one of the is_next and is_previous can be true, else the function cancels.

        :param remote_chainfile_dto: a dto that contains all necessary information
        :param consumer: A consumer object to handle connections
        :param producer: A producer object to handle connections
        :return: None
        """
        if remote_chainfile_dto.is_next and remote_chainfile_dto.is_previous:
            return

        if not remote_chainfile_dto.is_next and not remote_chainfile_dto.is_previous:
            return

        if remote_chainfile_dto.is_next:
            ChainfileHandler.__setup_for_next_of_remote_link(
                remote_chainfile_dto.name_of_called_link,
                remote_chainfile_dto.remote_link_addr,
                consumer
            )

        if remote_chainfile_dto.is_previous:
            ChainfileHandler.__setup_for_previous_of_remote_link(remote_chainfile_dto.chainfile_model, producer)

    @staticmethod
    def __setup_for_next_of_remote_link(
            remote_link_address: str,
            name_of_called_link: str,
            consumer: Consumer,
    ):
        """
        If the chainlink residing here is a next chainlink, that means it needs to consume a queue
        on the remote chainlink to receive messages. As such it connects to that hosts rabbitmq instance
        and subscribes to a queue.
        The name of the called link is needed because routing keys always refer to the subscriber
        that should consume the routing key.

        :param remote_link_address: The remote links ip address
        :param name_of_called_link: The name of the link that was called with the original request
        :param consumer: A consumer object to set up connections
        :return:
        """
        connection = RabbitMQConnector.connect_to_rabbit_mq_instance(remote_link_address)
        subscriber = consumer.create_new_subscriber(connection, name_of_called_link)
        subscriber.start_subscriber()

    @staticmethod
    def __setup_for_previous_of_remote_link(chainfile_model: ChainfileModel, producer: Producer):
        """
        If the chainlink residing here is a previous chainlink, that means that a queue with the appropriate
        routing key needs to be set up on the local rabbit mq instance for the remote chainlink to subscribe to.
        :param chainfile_model: The chainfile model containing necessary information
        :param producer: A producer object to create a new publisher from that will initiate the queue
        :return:
        """
        producer.create_new_publisher(chainfile_model.chainlink_name)
