# watch-webcam

Simple script to watch the status of the webcam and do some actions.

- switches all Elgato key lights on/off
- pauses music player at start of call
- disables xscreensaver during call

You can configure it with a config file, the default looks like this:
```
video:
  devices:
    - /dev/video0
    - /dev/video1
    - /dev/video2
  applications:
    - cheese
    - MainThread
    - firefox
    - zoom
    - GeckoMain
    - teams
    - chrome
    - slack

xscreensaver:
  enabled: true

media:
  enabled: true

light:
  enabled: true
  brightness: 10
  color: 5500
```

The config file is also the only option of the command:
```
usage: watch-webcam [-h] [-c CONFIG]

Detects webcam use and acts on it

options:
  -h, --help           show this help message and exit
  -c, --config CONFIG
```
