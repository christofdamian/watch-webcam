#!/bin/env python3

import subprocess
import time
import re

import dbus
import dbus.service
import leglight
from slack import WebClient

allLights = leglight.discover(2)

def slack_meeting(state):
    slack = WebClient(token='YOUR-TOKEN')
    if state:
        status = {
            'status_text': 'in call',
            'status_emoji': ':google-meet:',
            'status_expiation': 0
        }
    else:
        status = {
            'status_text': '',
            'status_emoji': '',
            'status_expiation': 0
        }

    slack.api_call(
        api_method='users.profile.set',
        json={
            'profile': status
        }
    )

def fuser(filename):
    return subprocess.check_output(['fuser', '-v', filename], stderr=subprocess.STDOUT)

def video_state(filename):
    try:
        output = fuser(filename).decode('utf-8')
        print(filename+":"+output)
        return re.search(
            r'm (cheese|MainThread|firefox|zoom|GeckoMain|teams)',
            output,
            re.MULTILINE
            ) is not None
    except subprocess.CalledProcessError as e:
        return False


def switch_lights(state):
    for light in allLights:
        if state:
            light.on()
            light.brightness(10)
            light.color(5500)
        else:
            light.off()

def xscreensaver_off():
    print("switch xscreensaver off")
    subprocess.run(['xscreensaver-command', '-deactivate'])

def pause_player():
    player_service = None
    bus = dbus.SessionBus()
    for service in bus.list_names():
        if re.match('org.mpris.MediaPlayer2.', service):
            print(service)
            player_service = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
            break

    if player_service:
        player = dbus.Interface(player_service, 'org.mpris.MediaPlayer2.Player')
        try:
            player.Pause()
        except dbus.DBusException as e:
            print("can not find player?" + str(e))

previous_state = None

while True:
    new_state = video_state('/dev/video0') or video_state('/dev/video1') or video_state('/dev/video2')

    if new_state:
        xscreensaver_off()

    if new_state != previous_state:
        switch_lights(new_state)
        #slack_meeting(new_state)
        if new_state:
            pause_player()

        previous_state = new_state
    else:
        time.sleep(1)
