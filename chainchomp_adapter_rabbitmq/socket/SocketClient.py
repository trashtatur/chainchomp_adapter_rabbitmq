import asyncio
from typing import Optional

import socketio
from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.MessageDeserializer import MessageDeserializer
from chainchomplib.configlayer.ChainfileDeserializer import ChainfileDeserializer
from chainchomplib.data import SocketEvents

from chainchomp_adapter_rabbitmq.messaging.ChainfileHandler import ChainfileHandler
from chainchomp_adapter_rabbitmq.messaging.MessageHandler import MessageHandler
from chainchomp_adapter_rabbitmq.rabbitmq.RabbitMQConnector import RabbitMQConnector
from chainchomp_adapter_rabbitmq.rabbitmq.consumer.Consumer import Consumer
from chainchomp_adapter_rabbitmq.rabbitmq.producer.Producer import Producer
from chainchomp_adapter_rabbitmq.socket.Emitter import SocketEmitter

sio = socketio.AsyncClient()
URL = 'http://localhost:4410'
socket_emitter = SocketEmitter(sio)
consumer = Consumer()
producer = Producer(RabbitMQConnector.connect_to_rabbit_mq_instance())


@sio.on(SocketEvents.EMIT_TO_ADAPTER)
async def on_receive_message(data):
    message = MessageDeserializer.deserialize(data)
    if message is not None:
        MessageHandler.handle_outgoing_message(message, producer)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


@sio.on(SocketEvents.EMIT_LOCAL_CHAINFILE_TO_ADAPTER)
async def on_receive_local_chainfile(data):
    chainfile = ChainfileDeserializer.deserialize(data)
    if chainfile is not None:
        ChainfileHandler.handle_incoming_local_chainfile(chainfile, consumer, producer)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


@sio.on(SocketEvents.EMIT_REMOTE_CHAINFILE_TO_ADAPTER)
async def on_receive_remote_chainfile(data):
    chainfile = ChainfileDeserializer.deserialize(data)
    if chainfile is not None:
        ChainfileHandler.handle_incoming_remote_chainfile(chainfile)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


async def connect():
    await sio.connect(URL, headers={'CHAINCHOMP_ADAPTER': 'rabbitmq'})


def get_emitter() -> SocketEmitter:
    return socket_emitter


loop = asyncio.get_event_loop()
loop.create_task(connect())
loop.run_forever()

