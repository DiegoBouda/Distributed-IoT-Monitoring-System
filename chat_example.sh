#!/bin/bash
# chat_example.sh - Starts the MQTT container, chat server, and chat client

# Optional: activate virtual environment
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Pull the latest HiveMQ Docker image
docker pull hivemq/hivemq4:latest

# Start (or ensure) the HiveMQ container is running
docker start frosty_albattani >/dev/null 2>&1 || \
docker run -d --name frosty_albattani -p 1883:1883 -p 8000:8000 -p 8080:8080 hivemq/hivemq4:latest

# Give broker a few seconds to boot up
sleep 3

# Start the chat server
python3 ./chat/chat_server.py > chat_example.log 2>&1 &

# Start the chat client
python3 ./client/chat_client.py >> chat_example.log 2>&1 &
