import time
import network
import ntptime
from machine import Pin


class Microcontroller:
    def __init__(self, SSID, KEY):
        print(f"Initialising the Microcontroller.")
        self.SSID = SSID
        self.KEY = KEY
        self.sta_if = network.WLAN(network.STA_IF)
        self.connectToWifi()
        self.setTime()
        self.setResetPin()

    def connectedToWifi(self):
        return self.sta_if.isconnected()

    def connectToWifi(self):
        if not self.connectedToWifi():
            try:
                print(f"Enabling WiFi on the Microcontroller.")
                self.sta_if.active(True)
                print(f"Connecting to {self.SSID}.")
                self.sta_if.connect(self.SSID, self.KEY)
                while not self.sta_if.isconnected():
                    pass
                print(f"WiFi connected successfully: {self.sta_if.ifconfig()}")
            except Exception as e:
                print(f"Could not connect to the WiFi. Error: {e}")
        else:
            print(f"WiFi already connected.")

    def setTime(self):
        if not self.connectedToWifi():
            print(
                f"You first need to be connected to the internet to set the time using NTP."
            )
            print(f"Trying to connect automatically for you.")
            self.connectToWifi()
        else:
            print(f"Automatically setting the time using NTP.")
            ntptime.settime()
            print(f"The current local time is: {time.localtime()}")

    def setResetPin(self):
        print(f"Setting the reset pin to HIGH so the OLED can work.")
        try:
            reset_pin = Pin(4)
            reset_pin.value(1)
            print(f"Reset pin set to HIGH successfully.")
        except Exception as e:
            print(f"Error while setting reset pin to HIGH: {e}")
