#!/bin/env python3

"""Main entry point for the watch-webcam"""

import argparse
import time
import logging
import yaml


from watch_webcam.video import Video
from watch_webcam.actions.xscreensaver import XScreenSaver
from watch_webcam.actions.media import Media
from watch_webcam.actions.light import Light

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ACTIONS = [XScreenSaver, Media, Light]


def main():
    """Main entry point for the watch-webcam"""

    parser = argparse.ArgumentParser(
        prog="watch-webcam",
        description="Detects webcam use and acts on it"
    )
    parser.add_argument("-c", "--config", default="watch-webcam.yml")
    parser.add_argument("-l", "--logging", default="WARNING")
    args = parser.parse_args()

    logger.setLevel(args.logging.upper())

    with open(args.config, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    video = Video(**config["video"])

    actions = []
    for action in ACTIONS:
        params = config[action.__name__.lower()]
        if params["enabled"]:
            del params["enabled"]
            actions.append(action(**params))

    for action in actions:
        action.discover()

    logger.info("Entering busy loop")

    previous_state = None
    while True:
        new_state = video.is_on()
        if new_state:
            for action in actions:
                action.while_on()

        if new_state != previous_state:
            logger.info("State switching: %s", new_state)
            for action in actions:
                action.switch(new_state)

            previous_state = new_state
        else:
            time.sleep(1)


if __name__ == '__main__':
    main()
