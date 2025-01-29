"""Module to pause media player"""

import re
import dbus
import dbus.service

from watch_webcam.actions.base import Base

class Media(Base):
    """Class to find and pause media player"""

    def find_player_service(self):
        """Find media service"""
        bus = dbus.SessionBus()
        for service in bus.list_names():
            if re.match('org.mpris.MediaPlayer2.', service):
                return dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
        return None

    def pause_player(self):
        """Pause all media players"""

        player_service = self.find_player_service()
        if player_service:
            player = dbus.Interface(player_service, 'org.mpris.MediaPlayer2.Player')
            try:
                player.Pause()
            except dbus.DBusException as error:
                print("Can not find player? ", type(error).__name__, "–", error)

    def switch(self, new_state):
        """Overriding the base class to pause the player, whenever a camera is on"""
        if new_state:
            self.pause_player()
