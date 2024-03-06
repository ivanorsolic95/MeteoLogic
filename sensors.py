import dht
import bmp085
import mq135
import machine
import time
from API import sendData


class DHT11:
    def __init__(self, pin_number):
        self.pin = machine.Pin(pin_number)
        self.sensor = dht.DHT11(self.pin)

    def getTemperature(self):
        self.sensor.measure()
        return self.sensor.temperature()

    def getHumidity(self):
        self.sensor.measure()
        return self.sensor.humidity()

    def getTemperatureHumidity(self):
        return self.getTemperature(), self.getHumidity()

class BMP180:
  def __init__(self, scl_number, sda_number):
      self.i2c = machine.SoftI2C(scl=machine.Pin(scl_number), sda=machine.Pin(sda_number))
      self.bmp = bmp085.BMP180(self.i2c)

  def getPressure(self):
     self.bmp.oversample = 2
     self.bmp.sealevel = 101325
     self.bmp.blocking_read()
     return self.bmp.pressure 
   
class MQ135:
   def __init__(self, pin_adc_number):
      self.mq135 = mq135.MQ135(machine.Pin(pin_adc_number))

   def getPPM(self):
      return self.mq135.get_ppm()
   
class SensorManager(DHT11, BMP180, MQ135):
   def __init__(self, dht_pin, bmp_scl, bmp_sda, mq135_pin_adc):
      DHT11.__init__(self, dht_pin)
      BMP180.__init__(self, bmp_scl, bmp_sda)
      MQ135.__init__(self, mq135_pin_adc)
      self.history = {'temperature': [], 'humidity': [], 'pressure': [], 'co2_ppm': [], 'time': []}
      self.interval = 600
   
   def measure(self):
       try: 
        current_temperature, current_humidity = self.getTemperatureHumidity()
        current_pressure = self.getPressure()
        current_ppm = self.getPPM()
        current_datetime = time.localtime()
        self.history['temperature'].append(current_temperature)
        self.history['humidity'].append(current_humidity)
        self.history['pressure'].append(current_pressure)
        self.history['co2_ppm'].append(current_ppm)
        self.history['time'].append(current_datetime)
       except Exception as e:
          print(f"Failed to read from the sensors: {e}")
  
   def getDataPeriodically(self):
        while True:
          try:
            self.measure()
            print(f"Data measured at {time.localtime()}")
            sendData(self.history)
            print(self.history)
            self.history = {'temperature': [], 'humidity': [], 'pressure': [], 'CO2_ppm': [], 'time': []}
            time.sleep(self.interval)
          except Exception as e:
             print(f"Failed to read or to send data: {e}")  
 