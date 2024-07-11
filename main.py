"""
Main script for the Hey-C running on a Raspberry Pi 4.
When this script is started, the air conditioning unit should
be off.
"""


from time import sleep

from utils.actions import get_temperature, push_button
from utils.logger import get_custom_logger
from settings import temperature_bound_lower, temperature_bound_upper


if __name__ == "__main__":
    logger = get_custom_logger()

    ac_currently_on = False
    while True:
        temperature_current = get_temperature()
        if (ac_currently_on and temperature_current < temperature_bound_lower) or (not ac_currently_on and temperature_current > temperature_bound_upper):
            push_button()
            ac_currently_on = not ac_currently_on
            logger.info(f"pushed button at temperature of {temperature_current}; ac should now be {ac_currently_on}")
        else:
            logger.info(f"temperature is {temperature_current}; not pushing button")
        sleep(60)
