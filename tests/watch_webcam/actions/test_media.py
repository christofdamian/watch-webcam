"""Tests for the Media class"""

import pytest
from unittest.mock import patch, MagicMock, call

from watch_webcam.actions.media import Media


@pytest.fixture
def mock_dbus_session_bus():
    """Create a mock for dbus.SessionBus"""
    with patch('dbus.SessionBus') as mock_bus:
        # Create a mock bus that can be returned by SessionBus()
        mock_session = MagicMock()
        mock_bus.return_value = mock_session
        
        # Set up the mock_session.list_names method
        mock_session.list_names.return_value = []
        
        yield mock_bus, mock_session


@pytest.fixture
def media_controller():
    """Create a Media controller instance"""
    return Media()


def test_find_player_service_with_match(mock_dbus_session_bus, media_controller):
    """Test finding a media player service when one exists"""
    mock_bus, mock_session = mock_dbus_session_bus
    
    # Set up the mock session to return a media player service
    mock_session.list_names.return_value = [
        'org.freedesktop.DBus', 
        'org.mpris.MediaPlayer2.spotify'
    ]
    
    # Create a mock object to be returned by get_object
    mock_player_object = MagicMock()
    mock_session.get_object.return_value = mock_player_object
    
    # Call the method under test
    result = media_controller.find_player_service()
    
    # Verify the result and method calls
    assert result == mock_player_object
    mock_session.list_names.assert_called_once()
    mock_session.get_object.assert_called_once_with(
        'org.mpris.MediaPlayer2.spotify', 
        '/org/mpris/MediaPlayer2'
    )


def test_find_player_service_without_match(mock_dbus_session_bus, media_controller):
    """Test finding a media player service when none exists"""
    mock_bus, mock_session = mock_dbus_session_bus
    
    # Set up the mock session to return no media player services
    mock_session.list_names.return_value = [
        'org.freedesktop.DBus', 
        'org.gnome.Shell'
    ]
    
    # Call the method under test
    result = media_controller.find_player_service()
    
    # Verify the result and method calls
    assert result is None
    mock_session.list_names.assert_called_once()
    mock_session.get_object.assert_not_called()


@patch('watch_webcam.actions.media.dbus.Interface')
def test_pause_player_with_service(mock_interface, media_controller):
    """Test pausing a player when a service is found"""
    # Mock find_player_service to return a mock player service
    with patch.object(media_controller, 'find_player_service') as mock_find:
        mock_player_service = MagicMock()
        mock_find.return_value = mock_player_service
        
        # Mock the player interface
        mock_player = MagicMock()
        mock_interface.return_value = mock_player
        
        # Call the method under test
        media_controller.pause_player()
        
        # Verify method calls
        mock_find.assert_called_once()
        mock_interface.assert_called_once_with(
            mock_player_service,
            'org.mpris.MediaPlayer2.Player'
        )
        mock_player.Pause.assert_called_once()


def test_pause_player_without_service(media_controller):
    """Test pausing a player when no service is found"""
    # Mock find_player_service to return None
    with patch.object(media_controller, 'find_player_service') as mock_find:
        mock_find.return_value = None
        
        # Call the method under test
        media_controller.pause_player()
        
        # Verify method calls
        mock_find.assert_called_once()


@patch('watch_webcam.actions.media.dbus.Interface')
def test_pause_player_with_dbus_exception(mock_interface, media_controller):
    """Test error handling when pausing a player"""
    # Mock find_player_service to return a mock player service
    with patch.object(media_controller, 'find_player_service') as mock_find:
        mock_player_service = MagicMock()
        mock_find.return_value = mock_player_service
        
        # Mock the player interface
        mock_player = MagicMock()
        mock_interface.return_value = mock_player
        
        # Set up the mock to raise an exception
        mock_player.Pause.side_effect = pytest.importorskip("dbus").DBusException("Test error")
        
        # Mock the logger
        with patch('watch_webcam.actions.media.logger') as mock_logger:
            # Call the method under test
            media_controller.pause_player()
            
            # Verify method calls
            mock_find.assert_called_once()
            mock_player.Pause.assert_called_once()
            # Check that warning was logged
            mock_logger.warning.assert_called_once()
            assert "Can not find player?" in mock_logger.warning.call_args[0][0]


def test_switch_on(media_controller):
    """Test switch method when state is True"""
    with patch.object(media_controller, 'pause_player') as mock_pause:
        # Call the method under test
        media_controller.switch(True)
        
        # Verify method calls
        mock_pause.assert_called_once()


def test_switch_off(media_controller):
    """Test switch method when state is False"""
    with patch.object(media_controller, 'pause_player') as mock_pause:
        # Call the method under test
        media_controller.switch(False)
        
        # Verify method calls
        mock_pause.assert_not_called()