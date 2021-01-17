from chainchomplib import LoggerInterface
from chainchomplib.exceptions.Exceptions import NotValidException
from chainchomplib.verify.SchemaVerifier import SchemaVerifier
from chainchomplib.verify.schema.MessageSchema import MessageSchema
from chainchomp_adapter_rabbitmq.socket.SocketEmitter import SocketEmitter


class IncomingMessageHandler:

    def __init__(self, socket_emitter: SocketEmitter):
        self.socket_emitter = socket_emitter

    def handle_incoming_message(self, data):
        try:
            SchemaVerifier.verify(data, MessageSchema())
        except NotValidException as exception:
            LoggerInterface.error(
                f'A message was not properly formatted when arriving on the rabbitmq adapter. '
                f'it will be ignored. Exception: {exception}'
            )
            return
        else:
            self.socket_emitter.emit_to_chainchomp_core(data)
