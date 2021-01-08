from pika.adapters.blocking_connection import BlockingChannel


class Subscriber:

    def __init__(self, channel: BlockingChannel, name: str, queue_name: str):
        self.channel = channel
        self.name = name
        self.queue_name = queue_name

    def start_subscriber(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_message,
            auto_ack=True
        )
        self.channel.start_consuming()

    def stop_subscriber(self):
        self.channel.stop_consuming()

    def on_message(self):
        pass
