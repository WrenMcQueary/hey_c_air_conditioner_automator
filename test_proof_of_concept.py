"""
Proof of concept
"""


from time import sleep

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import RPi.GPIO as GPIO


# Set up MCP3008 ADC
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)


# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

while True:
    voltage = channel.voltage
    print(voltage)
    if voltage > 1.5:
        print("High")
        GPIO.output(14, GPIO.HIGH)
    else:
        print("Low")
        GPIO.output(14, GPIO.LOW)
    sleep(1)
