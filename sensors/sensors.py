from time import sleep
from unittest.mock import Mock
from PIL import Image
from threading import Thread
from randomDHT import randomDHT
import paho.mqtt.client as paho
from io import BytesIO
import base64

class Sensor():

  def __init__(self, sensor_id="sensor1", camera = None , dht = None, pic_rate=1, dht_rate=1 ):
    if camera is None:
      self.init_camera()
    else:
      self.camera = camera
    if dht is None:
      self.init_dht()
    else:
      self.dht = dht
    
    self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
    self.client.on_connect = self.on_connect
    self.client.on_publish = self.on_publish

    host="localhost"
    port=1883

    self.client.connect(host,port)
    self.client.loop_start()
    
    self.pic_sleep= 1.0 / pic_rate
    self.dht_sleep = 1.0 / dht_rate

    base = f"forest/{sensor_id}"
    self.temp_topic = f"{base}/temperature"
    self.humidity_topic = f"{base}/humidity"
    self.light_topic = f"{base}/light"
    self.image_topic = f"{base}/image"

  def init_dht(self):
    #Ellie - Todo
    self.dht = randomDHT()
    
  def init_camera(self):
    from picamera2 import Picamera2
    self.camera = Picamera2()
    self.camera.start()
    sleep(1)

    print("Camera Initialized")


  def take_photo(self):
      image = self.camera.capture_image()

      buffer = BytesIO()
      image.save(buffer, format="JPEG")
      buffer.seek(0)
      image_bytes = buffer.read()

      image_b64 = base64.b64encode(image_bytes).decode('utf-8')

      self.client.publish(self.image_topic, image_b64, qos=1)

  def read_dht(self):
    '''Process Temperature and Humidity Data'''
    temp = self.dht.read_temperature()
    humidity = self.dht.read_humidity()
    light = self.dht.read_light()
    print(f'temp: {temp} humid: {humidity} light: {light}')
    self.client.publish(self.temp_topic, temp, 1)
    self.client.publish(self.humidity_topic, humidity, 1)
    self.client.publish(self.light_topic, light, 1)

  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully")
    else:
      print(f"Failed to connect, return code {rc}")

  def on_publish(self, client, userdata, mid):
    print(f"Message published successfully (MID: {mid})")


  def photo_loop(self):
    while True:
      self.take_photo()
      sleep(self.pic_sleep)

  def dht_loop(self):
    while True:
      self.read_dht()
      sleep(self.dht_sleep)

  def start(self):
    self.t1 = Thread(target=self.photo_loop)
    self.t2 = Thread(target=self.dht_loop)
    self.t1.start()
    self.t2.start()

if __name__ == "__main__":

  mock_camera = Mock()
  mock_camera.capture_image.return_value = Image.open("xena.jpg")
  
  dht = randomDHT()

  sensor1 = Sensor(sensor_id="sensor1", camera=mock_camera, dht=dht)
  sensor2 = Sensor(sensor_id="sensor2", camera=mock_camera, dht=dht)
  sensor3 = Sensor(sensor_id="sensor3", camera=mock_camera, dht=dht)

  sensor1.start() 
  sensor2.start()
  sensor3.start()

  try:
    while True:
      sleep(1)
  except KeyboardInterrupt:
    print("Stopping all sensors")