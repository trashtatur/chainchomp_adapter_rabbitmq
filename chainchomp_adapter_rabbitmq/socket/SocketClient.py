import asyncio
import socketio
from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.MessageDeserializer import MessageDeserializer
from chainchomplib.adapterlayer.RemoteChainfileDTODeserializer import RemoteChainfileDTODeserializer
from chainchomplib.configlayer.ChainfileDeserializer import ChainfileDeserializer
from chainchomplib.data import SocketEvents

from chainchomp_adapter_rabbitmq.messaging.ChainfileHandler import ChainfileHandler
from chainchomp_adapter_rabbitmq.messaging.OutgoingMessageHandler import OutgoingMessageHandler
from chainchomp_adapter_rabbitmq.rabbitmq.RabbitMQConnector import RabbitMQConnector
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Consumer import Consumer
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Producer import Producer
from chainchomp_adapter_rabbitmq.socket.SocketEmitter import SocketEmitter

sio = socketio.AsyncClient(engineio_logger=True)
URL = 'http://localhost:4410'
socket_emitter = SocketEmitter(sio)
consumer = Consumer(socket_emitter)
producer = Producer(RabbitMQConnector.connect())


@sio.on(SocketEvents.EMIT_TO_ADAPTER)
async def on_receive_message(data):
    message = MessageDeserializer.deserialize(data)
    if message is not None:
        OutgoingMessageHandler.handle_outgoing_message(message, producer)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


@sio.on(SocketEvents.EMIT_LOCAL_CHAINFILE_TO_ADAPTER)
async def on_receive_local_chainfile(data):
    chainfile = ChainfileDeserializer.deserialize(data)
    if chainfile is not None:
        ChainfileHandler.handle_incoming_local_chainfile(chainfile, consumer)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


@sio.on(SocketEvents.EMIT_REMOTE_CHAINFILE_TO_ADAPTER)
async def on_receive_remote_chainfile(data):
    remote_chainfile_dto = RemoteChainfileDTODeserializer.deserialize(data)
    if remote_chainfile_dto is not None:
        ChainfileHandler.handle_incoming_remote_chainfile(remote_chainfile_dto, consumer)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


async def connect():
    await sio.connect(URL, headers={'CHAINCHOMP_ADAPTER': 'chainchomp_rabbitmq'}, )
    await sio.wait()


def get_emitter() -> SocketEmitter:
    return socket_emitter


loop = asyncio.get_event_loop()
loop.create_task(connect())
loop.run_forever()

