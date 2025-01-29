from unittest.mock import patch

from watch_webcam.actions.xscreensaver import XScreenSaver
import subprocess

@patch("subprocess.run")
def test_deactivate(mock):
   XScreenSaver().deactivate()
   subprocess.run.assert_called_once_with(
       ['xscreensaver-command', '-deactivate'],
       stdout=subprocess.DEVNULL,
       check=False
   )


@patch.object(XScreenSaver, "deactivate")
def test_while_on(mock):
    xscreensaver = XScreenSaver()
    xscreensaver.while_on()
    xscreensaver.deactivate.assert_called_once_with()
