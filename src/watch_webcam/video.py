import subprocess
import re

class Video:
    def __init__(self):
        self.cameras = ["/dev/video0", "/dev/video1", "/dev/video2"]
        self.programs = ["cheese", "MainThread", "firefox", "zoom", "GeckoMain", "teams", "chrome", "slack"]

    def fuser(self, filename):
        try:
            return subprocess.check_output(['fuser', '-v', filename], stderr=subprocess.STDOUT).decode("utf-8")
        except subprocess.CalledProcessError as e:
            return ""

    def video_state(self, filename):
        output = self.fuser(filename)
        return any([output.find(program)>=0 for program in self.programs])

    def is_on(self):
        return any([self.video_state(filename) for filename in self.cameras])
