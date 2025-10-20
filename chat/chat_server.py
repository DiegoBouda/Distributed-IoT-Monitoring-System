import asyncio
import signal
from websockets import serve, exceptions
from datetime import datetime
import json


class EchoBroadcaster:
    def __init__(self):
        self.server = None
        self.channel_history = {}
        self.connections = {}

    async def echo(self, websocket):
        try:
            init_msg = await websocket.recv()
            init_data = json.loads(init_msg)
        except Exception as e:
            print(f"Connection initialization error: {e}")
            return

        username = init_data.get("username", "Anonymous")
        channel = init_data.get("channel", "general")

        self.connections[websocket] = channel
        self.channel_history.setdefault(channel, [])

        for msg in self.channel_history[channel]:
            await websocket.send(json.dumps(msg))

        try:
            async for message in websocket:
                data = json.loads(message)

                if data.get("type") == "switch_channel":
                    new_channel = data["channel"]
                    self.connections[websocket] = new_channel
                    self.channel_history.setdefault(new_channel, [])
                    for msg in self.channel_history[new_channel]:
                        await websocket.send(json.dumps(msg))
                    continue

                msg_obj = {
                    "type": "message",
                    "channel": self.connections[websocket],
                    "username": username,
                    "text": data["text"],
                    "timestamp": datetime.now().isoformat()
                }

                self.channel_history[self.connections[websocket]].append(msg_obj)

                for conn, conn_channel in self.connections.items():
                    if conn_channel == self.connections[websocket]:
                        await conn.send(json.dumps(msg_obj))

        finally:
            self.connections.pop(websocket, None)

    async def serve(self):
        async with serve(self.echo, "localhost", 8765) as server:
            stop_event = asyncio.Event()

            def handle_stop():
                stop_event.set()

            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, handle_stop)
            loop.add_signal_handler(signal.SIGTERM, handle_stop)

            await stop_event.wait()

            server.close()
            await server.wait_closed()

if __name__ == "__main__":
    broadcaster = EchoBroadcaster()
    try:
        asyncio.run(broadcaster.serve())
    except KeyboardInterrupt:
        print("Exited via keyboard interrupt.")