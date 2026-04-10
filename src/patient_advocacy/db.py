"""Database layer — local SQLite only."""

import sqlite3
from pathlib import Path
from .config import settings


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or settings.db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    _init_tables(conn)
    return conn


def _init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS drug_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_a TEXT NOT NULL,
            drug_b TEXT NOT NULL,
            severity TEXT,
            description TEXT,
            source TEXT DEFAULT 'FDA'
        );
        CREATE TABLE IF NOT EXISTS patient_rights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            source_url TEXT
        );
    """)
    conn.commit()
