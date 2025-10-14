# Introduction

A team of scientists is working on monitoring the local forest. 
They have built the sensor platforms using raspberry pis, and they are currently set up to read the sensor data and take pictures.
They are not doing anything with the data, currently, and they have come to you for help.

# Base Requirements

## Chat

The dashboard has a chat window to allow users to converse while looking at the data

 - Chat must be implemented using WebSockets
 - Chat must support multiple channels
 - Chat should identify messages by user name
 - Conversation history should be persistent

## Data Collection

 - Data Collection must use MQTT
 - Data must be filterable by sensor, and type of data.
 - Sensors are set up to read the following data: temperature, humidity and light level. All of which are floating point numbers.
 - Sensors are also set up to take pictures. 

# Prep Questions

## Chat

1. How will you format chat data so that you can meet all the requirements.
I will use a JSON-based message format that includes all necessary fields for identifying users, channels and message content. Each chat message will b represented as a dictionary like this:
{
    "types": "message",
    "channel": "temperature",
    "username": "Diego",
    "text": "Temperature rising at sensor #3",
    "timestam": "..."
}

2. How will you persist conversation history, and how will you communicate chat history on login
Conversation history will be persisted in server memory with a dictionary of message lists. Each channel stores its messages like this:
channel_history = {
    "general": [message1, message2, ...].
    "temperature": [messageA, messageB, ...],
    ...
}

When a user connects or switches to a channel, the server sends them the chat history for that channel via a WebSocket message. 

## Data Collection

1. What hosts will be subscribers and which will be publishers?
The sensor units (Raspberry Pis) will the be the publishers. Each Pi will read temperature, humidity, light level and capture images, then publish this data to the MQTT broker. 
The server or dashboard application will be the main subscriber. It will subscribes to sensor topics to collect, filter and display real-time data on the monitoring dashboard.  

2. What topics will you need to effectively communicate data?
A clear and hierarchial topic structure like this:
forest/<sensor_id>/<data_type>
Example topics:
forest/sensor01/temperature
forest/sensor01/humidity
forest/sensor01/light
forest/sensor01/image

3. Will you use wildcards at all in your topic structure? If yes, where and why?
Yes I will use wildcards to simpflify subscriptions and data filtering. 
Examples:
forest/+/temperature: Subscribe to temperature data from all sensors.
forest/sensor01/#: Subscribe to all data types (temperature, humidity, light, image) from sensor01.
forest/#: Subscribe to all data from all sensors. 

## Starter Code

Fork the starter code from [540/StarterCode/a2-distribute](https://gitlab.com/dawson-cst-cohort-2026/540/StarterCode/a2-distribute) into your Student Group.

1. In the sensors.py code how will you set up the connection to the MQTT broker?

2. In the sensors.py code, where will you publish/subscribe and what topics will you use?