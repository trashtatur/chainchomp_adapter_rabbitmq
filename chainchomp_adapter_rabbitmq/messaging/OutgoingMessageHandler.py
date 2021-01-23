from chainchomplib.adapterlayer.Message import Message
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Producer import Producer
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Publisher import Publisher


class OutgoingMessageHandler:

    @staticmethod
    def handle_outgoing_message(message: Message, producer: Producer):
        """
        A message comes in from a local chainlink to be sent to a remote
        chainlink. For that it needs to be sent through this adapter.

        This adapter thus pushes messages to an exchange on the local rabbitmq instance.
        The routing key corresponds to the individual recipient. That is because
        the recipient will subscribe to the queue named after him
        on this instance of rabbitmq.

        :param message: A message containing information needed to submit it
        :param producer: A producer instance
        :return: None
        """
        recipients = message.message_header.recipients
        for recipient in recipients:
            recipient_name = recipient.split('::')[1]
            if recipient not in producer.publishers:
                OutgoingMessageHandler.__prepare_publisher(producer, recipient_name)
            publisher: Publisher = producer.publishers[recipient_name]
            if publisher is None:
                return
            publisher.publish(message, recipient_name)

    @staticmethod
    def __prepare_publisher(producer: Producer, recipient: str):

        producer.create_new_publisher(recipient)
