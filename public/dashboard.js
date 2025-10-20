var hostname = "localhost";
var port = 8000;
var clientId = "jsClient-" + Math.floor(Math.random() * 1000);

var client = new Paho.MQTT.Client(hostname, Number(port), clientId);

var currentSensor = "sensor1";
var currentType = "temperature";

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({onSuccess: onConnect});

function onConnect() {
  console.log("Connected to MQTT broker");
  subscribeToTopic(currentSensor, currentType);
}

function subscribeToTopic(sensor, type) {
  const topic = `forest/${sensor}/${type}`;
  client.subscribe(topic, { qos: 1 });
  
  currentSensor = sensor;
  currentType = type;

  console.log(`Subscribed to topic: ${topic}`);
}

function unsubscribeFromTopic(sensor, type) {
  const topic = `forest/${sensor}/${type}`;
  client.unsubscribe(topic);
  console.log(`Unsubscribed from topic: ${topic}`);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function onMessageArrived(message) {
  const topic = message.destinationName;
  const parts = topic.split('/');  

  if (parts[parts.length - 1] === "image") {
    const base64Data = message.payloadString;  
    const img = document.getElementById("sensor-image") || document.createElement("img");
    img.id = "sensor-image";
    img.style.maxWidth = "300px";
    img.src = "data:image/jpeg;base64," + base64Data;
    document.body.appendChild(img);
    return;
  }

  console.log(`${topic}: ${message.payloadString}`);
}