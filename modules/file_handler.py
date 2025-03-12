import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import Callable, List
from ..gui.notification_manager import NotificationManager

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, organizer, notification_callback: Callable = None):
        self.organizer = organizer
        self.notifier = NotificationManager()
        self.notification_callback = notification_callback
        self.last_handled = {}
        
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
            
        path = Path(event.src_path)
        if self._should_handle(path):
            self._handle_file(path)
            
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
            
        path = Path(event.src_path)
        if self._should_handle(path):
            self._handle_file(path)
            
    def on_moved(self, event):
        """Handle file move events"""
        if event.is_directory:
            return
            
        dest_path = Path(event.dest_path)
        if self._should_handle(dest_path):
            self._handle_file(dest_path)
            
    def _should_handle(self, path: Path) -> bool:
        """Determine if a file should be processed"""
        # Skip system and hidden files
        if path.name.startswith('.') or path.name.startswith('~'):
            return False
            
        # Skip recently handled files
        current_time = time.time()
        last_handled = self.last_handled.get(path.name, 0)
        
        # Throttle handling to once per 5 seconds per file
        if current_time - last_handled < 5:
            return False
            
        self.last_handled[path.name] = current_time
        return True
        
    def _handle_file(self, path: Path) -> None:
        """Process a file that needs handling"""
        try:
            # Organize the file
            self.organizer._process_files(path.parent, None)
            
            # Notify about the change
            message = f"File {path.name} was organized"
            self.notifier.show_notification("File Organized", message)
            
            if self.notification_callback:
                self.notification_callback(path)
                
        except Exception as e:
            self.notifier.show_notification(
                "Organization Error",
                f"Failed to process {path.name}: {str(e)}"
            )

class FileMonitor:
    def __init__(self, organizer, paths: List[Path]):
        self.organizer = organizer
        self.paths = paths
        self.observer = Observer()
        self.handlers = []
        
    def start(self, notification_callback: Callable = None):
        """Start monitoring the specified paths"""
        for path in self.paths:
            if not path.exists():
                continue
                
            event_handler = FileEventHandler(
                self.organizer,
                notification_callback
            )
            
            self.handlers.append(event_handler)
            self.observer.schedule(
                event_handler,
                str(path),
                recursive=False
            )
            
        self.observer.start()
        
    def stop(self):
        """Stop all monitoring"""
        self.observer.stop()
        self.observer.join()
        
    def add_path(self, path: Path):
        """Add a new path to monitor"""
        if not path.exists():
            return
            
        event_handler = FileEventHandler(self.organizer)
        self.handlers.append(event_handler)
        self.observer.schedule(
            event_handler,
            str(path),
            recursive=False
        )
        
    def remove_path(self, path: Path):
        """Remove a path from monitoring"""
        for handler in self.handlers:
            if handler.path == path:
                self.observer.unschedule(handler)
                self.handlers.remove(handler)
                break