"""This module checks video devices for access by video call software"""

import subprocess

class Video:
    """This class handles checking the programs accessing video devices"""

    def __init__(self):
        self.cameras = ["/dev/video0", "/dev/video1", "/dev/video2"]
        self.programs = [
            "cheese",
            "MainThread",
            "firefox",
            "zoom",
            "GeckoMain",
            "teams",
            "chrome",
            "slack",
        ]

    def fuser(self, filename):
        """Returns fuser string for device"""
        return subprocess.run(
            ['fuser', '-v', filename],
            check=False,
            capture_output=True).stderr.decode("utf-8")
    def video_state(self, filename):
        """Returns if the video device is currently accessed by one of the programs"""

        output = self.fuser(filename)
        return any(output.find(program)>=0 for program in self.programs)

    def is_on(self):
        """Checks if any of the devices are currently accessed by one of the programs"""
        return any(self.video_state(filename) for filename in self.cameras)
