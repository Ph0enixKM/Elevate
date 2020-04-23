#!/usr/bin/env python3

import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        print(await websocket.recv())

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:8765'))