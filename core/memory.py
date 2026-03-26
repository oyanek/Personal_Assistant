from __future__ import annotations
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("db/ai_os.db")

class MemoryStore:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    amount REAL,
                    category TEXT,
                    description TEXT
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent TEXT,
                    action TEXT,
                    result TEXT,
                    timestamp TEXT
                )
                """
            )

    def add_message(self, role: str, content: str, timestamp: Optional[str] = None) -> int:
        timestamp = timestamp or datetime.utcnow().isoformat()
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
                (role, content, timestamp),
            )
            return cursor.lastrowid

    def get_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()][::-1]

    def add_transaction(self, date: str, amount: float, category: str, description: str) -> int:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO transactions (date, amount, category, description) VALUES (?, ?, ?, ?)",
                (date, amount, category, description),
            )
            return cursor.lastrowid

    def list_transactions(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM transactions ORDER BY date DESC")
        return [dict(row) for row in cursor.fetchall()]

    def add_agent_log(self, agent: str, action: str, result: str, timestamp: Optional[str] = None) -> int:
        timestamp = timestamp or datetime.utcnow().isoformat()
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO agent_logs (agent, action, result, timestamp) VALUES (?, ?, ?, ?)",
                (agent, action, result, timestamp),
            )
            return cursor.lastrowid
