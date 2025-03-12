import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Callable
from watchdog.observers import Observer
from .security import FileVault
from .rule_engine import RuleEngine
from .file_handler import FileMonitor

class DesktopOrganizer:
    def __init__(self, config_path: str = "config/categories.json"):
        self.config = self._load_config(config_path)
        self.vault = FileVault()
        self.rule_engine = RuleEngine()
        self.logger = self._setup_logger()
        self.monitor = None
        
    def start_monitoring(self, paths: List[Path], notification_callback: Callable = None):
        """Start monitoring specified paths for changes"""
        if self.monitor:
            self.monitor.stop()
            
        self.monitor = FileMonitor(self, paths)
        self.monitor.start(notification_callback)
        
    def stop_monitoring(self):
        """Stop all file monitoring"""
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Config load failed: {str(e)}")
    
    def organize(self, directory: Path, rules: List[Dict] = None) -> None:
        """Main organization workflow"""
        self._validate_path(directory)
        self._reset_desktop(directory)
        self._create_containers(directory)
        self._process_files(directory, rules)
        
    def _validate_path(self, path: Path) -> None:
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Invalid directory: {path}")
            
    def _reset_desktop(self, directory: Path) -> None:
        for item in directory.iterdir():
            if item.is_dir() and item.name != 'System Volume Information':
                self._empty_folder(item)
                
    def _empty_folder(self, folder: Path) -> None:
        for file in folder.glob('*'):
            try:
                shutil.move(str(file), str(folder.parent))
            except Exception as e:
                self.logger.error(f"Reset failed for {file.name}: {str(e)}")
        try:
            folder.rmdir()
        except Exception as e:
            self.logger.error(f"Folder removal failed: {str(e)}")
    
    def _create_containers(self, directory: Path) -> None:
        for category in self.config['categories']:
            container = directory / category
            container.mkdir(exist_ok=True)
            (container / '.meta').write_text(json.dumps({
                'color': self.config['categories'][category]['color'],
                'icon': self.config['categories'][category]['icon']
            }))
    
    def _process_files(self, directory: Path, rules: List[Dict]) -> None:
        for file in directory.iterdir():
            if file.is_dir() or file.name.startswith('.'):
                continue
                
            if self.vault.is_encrypted(file):
                continue
                
            category = self._determine_category(file)
            self._move_file(file, directory / category)
            
            if rules:
                self.rule_engine.apply_rules(file, rules)
    
    def _determine_category(self, file: Path) -> str:
        # Categorization logic with fallback
        if file.suffix.lower() == '.exe':
            return self._categorize_executable(file)
            
        for category, data in self.config['categories'].items():
            if file.suffix.lower() in data['extensions']:
                return category
                
        return 'Uncategorized'
    
    def _categorize_executable(self, file: Path) -> str:
        name = file.stem.lower()
        for category, patterns in self.config['executable_rules'].items():
            if any(p in name for p in patterns):
                return category
        return 'Executables'
    
    def _move_file(self, src: Path, dest_dir: Path) -> None:
        try:
            if not dest_dir.exists():
                dest_dir.mkdir()
            shutil.move(str(src), str(dest_dir / src.name))
        except Exception as e:
            self.logger.error(f"Move failed: {src.name} -> {dest_dir}: {str(e)}")
    
    def start_monitoring(self, directory: Path) -> None:
        from .file_handler import FileEventHandler
        event_handler = FileEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=False)
        observer.start()
        observer.join()