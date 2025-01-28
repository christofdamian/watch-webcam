"""Module to handle switching all Elgato lights"""

import leglight

class Light:
    """Class to handle switching all Elgato lights"""

    def __init__(self):
        self.brightness = 10
        self.color = 5500
        self.discovery_timeout = 2
        self.all_lights = []

    def discover(self):
        """Discover lights"""
        self.all_lights = leglight.discover(timeout=self.discovery_timeout)

    def on(self):
        """Switch all lights on"""
        for light in self.all_lights:
            light.brightness(self.brightness)
            light.color(self.color)
            light.on()
            print("on")

    def off(self):
        """Switch all lights off"""
        for light in self.all_lights:
            light.off()

    def switch(self, state):
        """Switch lights depending on the state"""
        if state:
            self.on()
        else:
            self.off()
