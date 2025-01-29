"""This module checks video devices for access by video call software"""

import subprocess

class Video:
    """This class handles checking the applications accessing video devices"""

    DEFAULT_DEVICES = ["/dev/video0", "/dev/video1", "/dev/video2"]
    DEFAULT_APPLICATIONS = [
            "cheese",
            "MainThread",
            "firefox",
            "zoom",
            "GeckoMain",
            "teams",
            "chrome",
            "slack",
        ]

    def __init__(self, devices=None, applications=None):
        if devices is None:
            devices = Video.DEFAULT_DEVICES
        if applications is None:
            applications = Video.DEFAULT_APPLICATIONS
        self.devices = devices
        self.applications = applications

    def fuser(self, filename):
        """Returns fuser string for device"""
        return subprocess.run(
            ['fuser', '-v', filename],
            check=False,
            capture_output=True).stderr.decode("utf-8")
    def video_state(self, filename):
        """Returns if the video device is currently accessed by one of the applications"""

        output = self.fuser(filename)
        return any(output.find(program)>=0 for program in self.applications)

    def is_on(self):
        """Checks if any of the devices are currently accessed by one of the applications"""
        return any(self.video_state(filename) for filename in self.devices)
