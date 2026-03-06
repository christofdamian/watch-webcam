from unittest.mock import patch, mock_open, MagicMock
import yaml

from watch_webcam.cli import main

SAMPLE_CONFIG = {
    "video": {"devices": ["/dev/video0"], "applications": ["zoom"]},
    "xscreensaver": {"enabled": False},
    "media": {"enabled": False},
    "light": {"enabled": True, "brightness": 20, "color": 5000},
    "script": {"enabled": False},
}


@patch("watch_webcam.cli.time.sleep", side_effect=KeyboardInterrupt)
@patch("watch_webcam.cli.Video")
@patch("builtins.open", mock_open(read_data=yaml.dump(SAMPLE_CONFIG)))
@patch("sys.argv", ["watch-webcam", "-c", "test.yml"])
def test_only_enabled_actions_are_created(mock_video, mock_sleep):
    mock_light_cls = MagicMock()
    mock_light_cls.config_key = "light"
    mock_light_instance = MagicMock()
    mock_light_cls.return_value = mock_light_instance

    mock_video_instance = MagicMock()
    mock_video.return_value = mock_video_instance
    mock_video_instance.is_on.return_value = False

    with patch("watch_webcam.cli.ACTIONS", [mock_light_cls]):
        try:
            main()
        except KeyboardInterrupt:
            pass

    mock_light_cls.assert_called_once_with(brightness=20, color=5000)
    mock_light_instance.discover.assert_called_once()


@patch("watch_webcam.cli.time.sleep", side_effect=KeyboardInterrupt)
@patch("watch_webcam.cli.Video")
@patch("builtins.open", mock_open(read_data=yaml.dump({
    **SAMPLE_CONFIG,
    "light": {"enabled": False},
})))
@patch("sys.argv", ["watch-webcam", "-c", "test.yml"])
def test_no_actions_when_all_disabled(mock_video, mock_sleep):
    mock_light_cls = MagicMock()
    mock_light_cls.config_key = "light"

    mock_video_instance = MagicMock()
    mock_video.return_value = mock_video_instance
    mock_video_instance.is_on.return_value = False

    with patch("watch_webcam.cli.ACTIONS", [mock_light_cls]):
        try:
            main()
        except KeyboardInterrupt:
            pass

    mock_light_cls.assert_not_called()
