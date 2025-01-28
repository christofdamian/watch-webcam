"""Module to control XScreenSaver"""

import subprocess

class XScreenSaver: # pylint: disable=too-few-public-methods
    """Class to control XScreenSaver"""

    def deactivate(self):
        """Deactivate XScreenSaver - pretending that the user is active"""
        return subprocess.run(
            ['xscreensaver-command', '-deactivate'],
            stdout=subprocess.DEVNULL,
            check=False
        )
