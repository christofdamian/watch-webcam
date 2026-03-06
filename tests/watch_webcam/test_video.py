from unittest.mock import patch

from watch_webcam.video import Video


def test_default_devices():
    video = Video()
    assert video.devices == Video.DEFAULT_DEVICES


def test_default_applications():
    video = Video()
    assert video.applications == Video.DEFAULT_APPLICATIONS


def test_custom_devices_and_applications():
    video = Video(devices=["/dev/video5"], applications=["zoom"])
    assert video.devices == ["/dev/video5"]
    assert video.applications == ["zoom"]


@patch.object(Video, "fuser")
def test_video_state_on(mock_fuser):
    mock_fuser.return_value = "USER        PID ACCESS COMMAND\n/dev/video0: user  1234 F.... zoom"
    video = Video()
    assert video.video_state("/dev/video0") is True


@patch.object(Video, "fuser")
def test_video_state_off(mock_fuser):
    mock_fuser.return_value = ""
    video = Video()
    assert video.video_state("/dev/video0") is False


@patch.object(Video, "fuser")
def test_video_state_unknown_application(mock_fuser):
    mock_fuser.return_value = "USER        PID ACCESS COMMAND\n/dev/video0: user  1234 F.... unknownapp"
    video = Video()
    assert video.video_state("/dev/video0") is False


@patch.object(Video, "video_state")
def test_is_on_true(mock_state):
    mock_state.side_effect = [False, True, False]
    video = Video(devices=["/dev/video0", "/dev/video1", "/dev/video2"])
    assert video.is_on() is True


@patch.object(Video, "video_state")
def test_is_on_false(mock_state):
    mock_state.return_value = False
    video = Video(devices=["/dev/video0", "/dev/video1"])
    assert video.is_on() is False
