"""Main script for the Hey-C running on a Raspberry Pi 4.
When this script is started, the air conditioning unit should
be off.
"""


import util
from time import sleep


if __name__ == "__main__":
    ac_currently_on = False
    temperature_bound_upper = 72    # Fahrenheit
    temperature_bound_lower = 67    # Fahrenheit
    while True:
        temperature_current = util.get_temperature()
        if (ac_currently_on and temperature_current < temperature_bound_lower) or (not ac_currently_on and temperature_current > temperature_bound_upper):
            util.push_button()
            ac_currently_on = not ac_currently_on
        time.sleep(60)
