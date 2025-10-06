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

2. How will you persist conversation history, and how will you communicate chat history on login

## Data Collection

1. What hosts will be subscribers and which will be publishers?

2. What topics will you need to effectively communicate data?

3. Will you use wildcards at all in your topic structure? If yes, where and why?

## Starter Code

Fork the starter code from [540/StarterCode/a2-distribute](https://gitlab.com/dawson-cst-cohort-2026/540/StarterCode/a2-distribute) into your Student Group.

1. In the sensors.py code how will you set up the connection to the MQTT broker?

2. In the sensors.py code, where will you publish/subscribe and what topics will you use?