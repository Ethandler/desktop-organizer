import json
from pathlib import Path
from typing import Dict, List
import re

class RuleEngine:
    def __init__(self, rules_path: str = "config/rules.json"):
        self.rules = self._load_rules(rules_path)
        
    def _load_rules(self, path: str) -> List[Dict]:
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return []
            
    def apply_rules(self, file: Path, additional_rules: List[Dict] = None) -> None:
        all_rules = self.rules + (additional_rules or [])
        
        for rule in all_rules:
            if self._matches_rule(file, rule):
                self._execute_action(file, rule['action'])
                
    def _matches_rule(self, file: Path, rule: Dict) -> bool:
        conditions = rule.get('conditions', {})
        
        # Name matching
        if 'name_pattern' in conditions:
            if not re.search(conditions['name_pattern'], file.name):
                return False
                
        # Extension matching
        if 'extensions' in conditions:
            if file.suffix.lower() not in conditions['extensions']:
                return False
                
        # Size conditions
        if 'min_size' in conditions:
            if file.stat().st_size < conditions['min_size']:
                return False
                
        if 'max_size' in conditions:
            if file.stat().st_size > conditions['max_size']:
                return False
                
        return True
        
    def _execute_action(self, file: Path, action: Dict) -> None:
        action_type = action['type']
        
        if action_type == 'move':
            self._move_file(file, action['destination'])
        elif action_type == 'encrypt':
            self._encrypt_file(file, action.get('password'))
        elif action_type == 'notify':
            self._send_notification(file, action['message'])
            
    def _move_file(self, file: Path, destination: str) -> None:
        dest_path = file.parent / destination
        dest_path.mkdir(exist_ok=True)
        file.rename(dest_path / file.name)
        
    def _encrypt_file(self, file: Path, password: str = None) -> None:
        from .security import FileVault
        vault = FileVault()
        vault.encrypt_file(file, password or 'default')
        
    def _send_notification(self, file: Path, message: str) -> None:
        from ..gui.notification_manager import NotificationManager
        notifier = NotificationManager()
        notifier.show_notification("File Action", message.format(file=file.name))