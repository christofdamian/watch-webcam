"""Module to handle switching all Elgato lights"""


import logging
import leglight

from watch_webcam.actions.base import Base

logger = logging.getLogger("logger")


class Light(Base):
    """Class to handle switching all Elgato lights"""

    def __init__(self, brightness=10, color=5500, discovery_timeout=5):
        self.brightness = brightness
        self.color = color
        self.discovery_timeout = discovery_timeout
        self.all_lights = []

    def discover(self):
        """Discover lights"""
        self.all_lights = leglight.discover(timeout=self.discovery_timeout)

        logger.info("Discovered %d lights", len(self.all_lights))
        for light in self.all_lights:
            logger.debug("Found light: %s", light)

        if not self.all_lights:
            logger.warning("No lights discovered")

    def on(self):
        """Switch all lights on"""
        for light in self.all_lights:
            light.brightness(self.brightness)
            light.color(self.color)
            light.on()

    def off(self):
        """Switch all lights off"""
        for light in self.all_lights:
            light.off()

    def switch(self, new_state):
        """Switch lights depending on the state"""
        if new_state:
            self.on()
        else:
            self.off()
