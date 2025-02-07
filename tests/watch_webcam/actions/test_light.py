import pytest
from unittest.mock import Mock, patch
from watch_webcam.actions.light import Light


@pytest.fixture
def mock_light():
    """Fixture to create a mock light device"""
    light = Mock()
    light.brightness = Mock()
    light.color = Mock()
    light.on = Mock()
    light.off = Mock()
    return light


@pytest.fixture
def light_controller():
    """Fixture to create a Light controller instance"""
    return Light(brightness=50, color=6000, discovery_timeout=1)


def test_init():
    """Test Light class initialization"""
    light = Light(brightness=50, color=6000, discovery_timeout=2)
    assert light.brightness == 50
    assert light.color == 6000
    assert light.discovery_timeout == 2
    assert light.all_lights == []


@patch('watch_webcam.actions.light.leglight.discover')
def test_discover_with_lights(mock_discover, mock_light):
    """Test discover method when lights are found"""
    mock_discover.return_value = [mock_light]

    light_controller = Light()
    light_controller.discover()

    mock_discover.assert_called_once_with(timeout=5)
    assert len(light_controller.all_lights) == 1
    assert light_controller.all_lights[0] == mock_light


@patch('watch_webcam.actions.light.leglight.discover')
def test_discover_no_lights(mock_discover):
    """Test discover method when no lights are found"""
    mock_discover.return_value = []

    light_controller = Light()
    light_controller.discover()

    mock_discover.assert_called_once_with(timeout=5)
    assert light_controller.all_lights == []


def test_on(light_controller, mock_light):
    """Test turning lights on"""
    light_controller.all_lights = [mock_light]
    light_controller.on()

    mock_light.brightness.assert_called_once_with(light_controller.brightness)
    mock_light.color.assert_called_once_with(light_controller.color)
    mock_light.on.assert_called_once()


def test_off(light_controller, mock_light):
    """Test turning lights off"""
    light_controller.all_lights = [mock_light]
    light_controller.off()

    mock_light.off.assert_called_once()


def test_switch_on(light_controller):
    """Test switch method with state=True"""
    with patch.object(light_controller, 'on') as mock_on:
        light_controller.switch(True)
        mock_on.assert_called_once()


def test_switch_off(light_controller):
    """Test switch method with state=False"""
    with patch.object(light_controller, 'off') as mock_off:
        light_controller.switch(False)
        mock_off.assert_called_once()
