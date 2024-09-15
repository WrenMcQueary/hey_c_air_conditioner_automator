"""
Simple actions that the robot can perform.
"""


from time import sleep
from utils.low_level.temperature import TemperatureTable

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
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

temperature_table = TemperatureTable()


def get_temperature() -> float:
    """Return the temperature in degrees Fahrenheit
    """
    # Read voltage from the ADC
    voltage = channel.voltage
    # Convert to a temperature in Fahrenheit
    temperature = temperature_table.voltage_to_temperature(voltage)
    return temperature


def push_button(duration=0.1) -> None:
    """Actuate the motor to press and release the button on the
    air conditioning unit
    :param duration:        pulse duration in seconds
    """
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)
    sleep(duration)
    GPIO.output(15, GPIO.LOW)
