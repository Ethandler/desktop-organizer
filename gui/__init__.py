"""
Desktop Organizer GUI Package
Contains all graphical interface components
"""

from .main_window import DesktopOrganizerGUI
from .launchpad_view import LaunchpadView
from .notification_manager import NotificationManager

__all__ = ['DesktopOrganizerGUI', 'LaunchpadView', 'NotificationManager']