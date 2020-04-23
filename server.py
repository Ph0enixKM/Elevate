#!/usr/bin/env python3

import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message + '::FromServer')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()