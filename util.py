"""Simple utility classes and functions
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
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering.  The alternative is GPIO.setmode(GPIO.BCM), which uses "NAME" on the pinout diagram instead of "Pin#".
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin, and set initial value to low.
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)   # Set pin 10 to be an output pin, and set initial value to low.



def get_temperature() -> float:
    """Return the temperature in degrees Fahrenheit
    """
    # Read voltage from the ADC
    voltage = channel.voltage
    # Convert to a temperature in Fahrenheit
    pass    # TODO
    


def push_button() -> None:
    """Actuate the motor to press and release the button on the
    air conditioning unit
    """
    GPIO.output(14, GPIO.HIGH)
    sleep(1)
    GPIO.output(14, GPIO.LOW)
