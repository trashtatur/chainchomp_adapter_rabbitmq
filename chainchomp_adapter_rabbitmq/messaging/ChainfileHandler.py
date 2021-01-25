from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.data.RemoteChainfileDTO import RemoteChainfileDTO

from chainchomp_adapter_rabbitmq.rabbitmq.RabbitMQConnector import RabbitMQConnector
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Consumer import Consumer


class ChainfileHandler:

    @staticmethod
    def handle_incoming_local_chainfile(chainfile_model: ChainfileModel, consumer: Consumer):
        for previous_link in chainfile_model.previous_links:
            name_and_ip = previous_link.split('::')
            connection = RabbitMQConnector.connect(name_and_ip[0])
            subscriber = consumer.create_new_subscriber(connection, chainfile_model.chainlink_name)
            subscriber.start_subscriber()

    @staticmethod
    def handle_incoming_remote_chainfile(
            remote_chainfile_dto: RemoteChainfileDTO,
            consumer: Consumer
    ):
        """
        This interprets an incoming remote chainfile and prepares the adapter for anything related to that
        Only one of the is_next and is_previous can be true, else the function cancels.

        :param remote_chainfile_dto: a dto that contains all necessary information
        :param consumer: A consumer object to handle connections
        :return: None
        """
        if remote_chainfile_dto.is_next and remote_chainfile_dto.is_previous:
            return

        if not remote_chainfile_dto.is_next and not remote_chainfile_dto.is_previous:
            return

        if remote_chainfile_dto.is_next:
            ChainfileHandler.__setup_for_next_of_remote_link(
                remote_chainfile_dto.remote_link_addr,
                remote_chainfile_dto.name_of_called_link,
                consumer
            )

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
        connection = RabbitMQConnector.connect(remote_link_address)
        subscriber = consumer.create_new_subscriber(connection, name_of_called_link)
        subscriber.start_subscriber()
