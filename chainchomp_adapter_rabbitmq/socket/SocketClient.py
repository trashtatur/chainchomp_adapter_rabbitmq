import asyncio

import socketio
from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.MessageDeserializer import MessageDeserializer
from chainchomplib.data import SocketEvents

from chainchomp_adapter_rabbitmq.messaging.MessageHandler import MessageHandler
from chainchomp_adapter_rabbitmq.socket.Emitter import SocketEmitter

sio = socketio.AsyncClient()
URL = 'http://localhost:4410'
socket_emitter = SocketEmitter(sio)


@sio.on(SocketEvents.EMIT_TO_ADAPTER)
async def on_receive_message(data):
    message = MessageDeserializer.deserialize(data)
    if message is not None:
        MessageHandler.handle_incoming_message(message)
    else:
        LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored {data}')


@sio.on(SocketEvents.EMIT_LOCAL_CHAINFILE_TO_ADAPTER)
async def on_receive_local_chainfile(data):
    pass


@sio.on(SocketEvents.EMIT_REMOTE_CHAINFILE_TO_ADAPTER)
async def on_receive_remote_chainfile(data):
    pass


async def connect():
    await sio.connect(URL, headers={'CHAINCHOMP_ADAPTER': 'rabbitmq'})


def get_emitter() -> SocketEmitter:
    return socket_emitter


loop = asyncio.get_event_loop()
loop.create_task(connect())
loop.run_forever()

