from time import sleep
from unittest.mock import Mock
from PIL import Image
from threading import Thread

class Sensor():

  def __init__(self, camera = None , dht = None, pic_rate=1, dht_rate=1 ):
    if camera is None:
      self.init_camera()
    else:
      self.camera = camera
    if dht is None:
      self.init_dht()
    else:
      self.dht = dht
    
    self.pic_sleep= 1.0 / pic_rate
    self.dht_sleep = 1.0 / dht_rate

  def init_dht(self):
    #Ellie - Todo
    self.dht = None

  def init_camera(self):
    from picamera2 import Picamera2
    self.camera = Picamera2()
    self.camera.start()
    sleep(1)

    print("Camera Initialized")


  def take_photo(self):
    '''Process Image Data'''
    image = self.camera.capture_image()
    image.show()

  def read_dht(self):
    '''Process Temperature and Humidity Data'''
    print(f'temp: {self.dht.read_temperature()} humid: {self.dht.read_humidity()}')

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

    self.t1.join()
    self.t2.join()


if __name__ == "__main__":

  # Setting up mocks for sensors
  mock_camera = Mock()
  mock_camera.capture_image.return_value = Image.open("xena.jpg")
  
  dht = Mock()
  dht.read_temperature.return_value = 27.1
  dht.read_humidity.return_value=54.1

  sensor = Sensor(camera=mock_camera, dht=dht)

  sensor.start()