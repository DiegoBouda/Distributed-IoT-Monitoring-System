#!/bin/bash
# mqtt_example.sh - Starts the MQTT container, sensors, and MQTT client dashboard

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

# Start the sensors
python3 ./sensors/sensors.py > mqtt_example.log 2>&1 &

# Start the MQTT client dashboard
python3 ./client/mqtt_client.py >> mqtt_example.log 2>&1 &