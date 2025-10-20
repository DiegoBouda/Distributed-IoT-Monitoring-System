import asyncio
import websockets
import json
import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def chat_client(username="Anonymous", channel="general"):
    try:
        async with websockets.connect("ws://localhost:8000") as ws:
            logging.info("Connected to WebSocket server")

            init_msg = {
                "username": username,
                "channel": channel
            }
            await ws.send(json.dumps(init_msg))
            logging.info(f"Sent init message: {init_msg}")


            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                print(f"[{data.get('channel')}] {data.get('username')}: {data.get('text')}")
                logging.info(f"[{data.get('channel')}] {data.get('username')}: {data.get('text')}")

    except websockets.ConnectionClosed as e:
        logging.warning(f"WebSocket connection closed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Chat Client",
        description="Simple WebSocket chat client",
        epilog="Example: python chat_client.py --username Diego --channel general"
    )

    parser.add_argument("--username", "-u", default="Anonymous", help="Set your chat username")
    parser.add_argument("--channel", "-c", default="general", help="Set the chat channel to join")

    args = parser.parse_args()

    asyncio.run(chat_client(args.username, args.channel))
