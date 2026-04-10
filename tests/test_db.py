"""Tests for database layer."""

import sqlite3
import tempfile
from pathlib import Path

from patient_advocacy.db import get_connection


def test_creates_tables():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        conn = get_connection(db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "documents" in tables
        assert "drug_interactions" in tables
        assert "patient_rights" in tables
        conn.close()


def test_insert_document():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        conn = get_connection(db_path)
        conn.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", ("test.pdf", "sample content"))
        conn.commit()
        row = conn.execute("SELECT * FROM documents WHERE filename='test.pdf'").fetchone()
        assert row["content"] == "sample content"
        conn.close()
