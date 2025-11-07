from unittest.mock import patch
import os


from watch_webcam.actions.xscreensaver import XScreenSaver
import subprocess


@patch("subprocess.run")
@patch.dict(os.environ, {'DISPLAY': ':0'})
def test_deactivate(mock):
    XScreenSaver().deactivate()
    subprocess.run.assert_called_once_with(
        ['xscreensaver-command', '-deactivate'],
        stdout=subprocess.DEVNULL,
        check=False
    )


@patch("subprocess.run")
@patch.dict(os.environ, {}, clear=True)
def test_deactivate_without_display(mock):
    result = XScreenSaver().deactivate()
    subprocess.run.assert_not_called()
    assert result is None


@patch.object(XScreenSaver, "deactivate")
def test_while_on(mock):
    xscreensaver = XScreenSaver()
    xscreensaver.while_on()
    xscreensaver.deactivate.assert_called_once_with()
