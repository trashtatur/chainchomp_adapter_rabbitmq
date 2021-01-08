from chainchomplib.adapterlayer.Message import Message

from chainchomp_adapter_rabbitmq.rabbitmq.producer.Producer import Producer
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Publisher import Publisher


class MessageHandler:

    @staticmethod
    def handle_outgoing_message(message: Message, producer: Producer):
        recipients = message.message_header.recipients
        for recipient in recipients:
            publisher: Publisher = producer.publishers[recipient]
            if publisher is None:
                return
            publisher.produce(message, message.message_header.origin)
