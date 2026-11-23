import sqlite3
from pathlib import Path


class Memory:
    def __init__(self):
        project_dir = Path(__file__).resolve().parent.parent
        data_dir = project_dir / "data"
        data_dir.mkdir(exist_ok=True)

        self.db_path = data_dir / "nova_memory.db"

        with sqlite3.connect(self.db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save(self, role: str, content: str):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                (role, content)
            )

    def history(self, limit: int = 20):
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

        return [
            {"role": role, "content": content}
            for role, content in reversed(rows)
        ]