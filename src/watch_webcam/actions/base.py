"""Module for the action base class"""

class Base:
    """This class only provides default stubs for the availble methods"""

    def discover(self):
        """This is called before the main method to discover devices"""

    def while_on(self):
        """This is called in every loop, while a camera is on"""

    def switch(self, new_state):
        """This is called when the state switches between on/off (True/False)"""
