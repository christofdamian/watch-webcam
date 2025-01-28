#!/bin/env python3

"""Main entry point for the watch-webcam"""

import time

from video import Video
from xscreensaver import XScreenSaver
from media import Media
from light import Light

def main():
    """Main entry point for the watch-webcam"""

    video = Video()
    xscreensaver = XScreenSaver()
    media = Media()
    light = Light()
    light.discover()

    previous_state = None
    while True:
        new_state = video.is_on()
        if new_state:
            xscreensaver.deactivate()

        if new_state != previous_state:
            light.switch(new_state)
            if new_state:
                media.pause_player()

            previous_state = new_state
        else:
            time.sleep(1)


if __name__ == '__main__':
    main()
