"""Module to run scripts on webcam on/off events"""


import logging
import subprocess

from watch_webcam.actions.base import Base

logger = logging.getLogger("logger")


class Script(Base):
    """Class to run configurable scripts when webcam turns on or off"""

    config_key = "script"

    def __init__(self, on=None, off=None):
        self.on_scripts = on or []
        self.off_scripts = off or []

    def run(self, script):
        """Run a script, logging any errors"""
        logger.info("Running script: %s", script)
        try:
            subprocess.run(script, check=True, shell=True)
        except subprocess.CalledProcessError as error:
            logger.warning("Script failed: %s - %s", script, error)

    def switch(self, new_state):
        """Run the on or off scripts when webcam state changes"""
        scripts = self.on_scripts if new_state else self.off_scripts
        for script in scripts:
            self.run(script)
