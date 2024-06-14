"""
Repeatedly print the current temperature.
"""


from time import sleep

from utils.actions import get_temperature


while True:
    print(get_temperature())
    sleep(1)
