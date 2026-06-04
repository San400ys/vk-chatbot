import sqlite3
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
from config import config


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vk_user_id INTEGER NOT NULL,
                    user_name TEXT,
                    contact_info TEXT,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON feedback(vk_user_id)')

    def save_feedback(self, vk_user_id: int, user_name: str,
                      contact_info: str, message: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'INSERT INTO feedback (vk_user_id, user_name, contact_info, message) VALUES (?, ?, ?, ?)',
                (vk_user_id, user_name, contact_info, message)
            )
            return cursor.lastrowid

    def get_all_feedback(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM feedback ORDER BY created_at DESC LIMIT ?',
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]
