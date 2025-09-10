"""Module to handle switching all Elgato lights"""


import logging
import time
import leglight

from watch_webcam.actions.base import Base

logger = logging.getLogger("logger")


class Light(Base):
    """Class to handle switching all Elgato lights"""

    def __init__(self, brightness=10, color=5500, discovery_timeout=5, max_retries=3, retry_delay=2):
        self.brightness = brightness
        self.color = color
        self.discovery_timeout = discovery_timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.all_lights = []

    def discover(self):
        """Discover lights with retries"""
        for attempt in range(self.max_retries):
            self.all_lights = leglight.discover(timeout=self.discovery_timeout)
            
            logger.info("Discovered %d lights (attempt %d/%d)", len(self.all_lights), attempt + 1, self.max_retries)
            for light in self.all_lights:
                logger.debug("Found light: %s", light)
            
            if self.all_lights:
                return
            
            if attempt < self.max_retries - 1:
                logger.warning("No lights discovered, retrying in %d seconds...", self.retry_delay)
                time.sleep(self.retry_delay)
        
        logger.warning("No lights discovered after %d attempts", self.max_retries)

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
