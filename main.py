from sensors import SensorManager

sensors = SensorManager(dht_pin=16, bmp_scl=22, bmp_sda=21, mq135_pin_adc=36)

sensors.getDataPeriodically()

