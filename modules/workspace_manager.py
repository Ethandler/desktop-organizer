import json
from pathlib import Path
from typing import Dict, List
import sqlite3

class WorkspaceManager:
    def __init__(self, db_path: str = "workspaces.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workspaces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    config TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
    def create_workspace(self, name: str, config: Dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO workspaces (name, config) VALUES (?, ?)",
                (name, json.dumps(config))
            )
            
    def get_workspace(self, name: str) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT config FROM workspaces WHERE name = ?",
                (name,)
            )
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
            
    def list_workspaces(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name, created_at FROM workspaces")
            return [dict(row) for row in cursor.fetchall()]
            
    def delete_workspace(self, name: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM workspaces WHERE name = ?", (name,))