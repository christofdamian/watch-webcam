"""Module to control XScreenSaver"""

import subprocess

from watch_webcam.actions.base import Base

class XScreenSaver(Base):
    """Class to control XScreenSaver"""

    def deactivate(self):
        """Deactivate XScreenSaver - pretending that the user is active"""
        return subprocess.run(
            ['xscreensaver-command', '-deactivate'],
            stdout=subprocess.DEVNULL,
            check=False
        )

    def while_on(self):
        """Overriding base method, which is called while camera is on"""
        self.deactivate()
