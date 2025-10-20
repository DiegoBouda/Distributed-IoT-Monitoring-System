import paho.mqtt.client as paho
import logging
import argparse

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully")
        client.subscribe(userdata["topic"], qos=1)
    else:
        logging.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    
    if len(topic_parts) == 3:
        _, sensor, data_type = topic_parts

        if data_type == "image":
            logging.info(f"[{sensor}] Image received, saving as {sensor}_image.jpg")
            with open(f"{sensor}_image.jpg", "wb") as f:
                f.write(msg.payload)
            return 

        try:
            value = msg.payload.decode("utf-8")
        except UnicodeDecodeError:
            logging.warning(f"[{sensor}] Received non-text data for {data_type}, skipping")
            return

        if data_type == "temperature":
            logging.info(f"[{sensor}] Temperature: {value}°C")
        elif data_type == "humidity":
            logging.info(f"[{sensor}] Humidity: {value}%")
        elif data_type == "light":
            logging.info(f"[{sensor}] Light: {value} lux")
        else:
            logging.debug(f"[{sensor}] Unknown data type '{data_type}': {value}")
    else:
        logging.warning(f"Unexpected topic format: {msg.topic}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="MQTT Client",
        description="Simple MQTT client that listens to forest sensor data.",
        epilog="Example: python mqtt_client.py --host localhost --port 1883 --topic forest/+/+"
    )

    parser.add_argument("--topic", "-t", default="forest/+/+", help="MQTT topic to subscribe to (default: forest/+/+)")

    args = parser.parse_args()

    client = paho.Client(userdata={"topic": args.topic}, protocol=paho.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    host = "localhost"
    port = 1883

    client.connect(host, port)
    client.loop_forever()