import zmq
import zmq.asyncio

async def zmq_example():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    print("Socket created successfully")

import asyncio
asyncio.run(zmq_example())