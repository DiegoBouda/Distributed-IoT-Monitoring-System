import random

class randomDHT:

  def __init__(self):
    self.temp_max = 30
    self.temp_min = -30
    self.humid_min = 0
    self.humid_max = 100
    self.light_min = 0
    self.light_max = 1000

  def read_temperature(self):
    return random.random() * (self.temp_max - self.temp_min) + self.temp_min
  
  def read_humidity(self):
    return random.random() * (self.humid_max - self.humid_min) + self.humid_min
  
  def read_light(self):
    return random.random() * (self.light_max - self.light_min) + self.light_min