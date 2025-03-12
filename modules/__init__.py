"""
Desktop Organizer Core Modules
"""

from .core_organizer import DesktopOrganizer
from .security import FileVault
from .rule_engine import RuleEngine
from .scheduler import TaskScheduler
from .workspace_manager import WorkspaceManager
from modules import file_handler

__all__ = [
    'DesktopOrganizer',
    'FileVault',
    'RuleEngine',
    'TaskScheduler',
    'WorkspaceManager'
]