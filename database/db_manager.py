"""
db_manager.py
Manages the SQLite connection and schema creation.
The database file lives in ~/.budgetdesk/ to keep it separate from the source code.
"""
import sqlite3
from pathlib import Path

# ── Database location ────────────────────────────────────────────────────────
DB_DIR = Path.home() / ".budgetdesk"
DB_PATH = DB_DIR / "expenses.db"

# Categorías iniciales según AGENTS.md
_DEFAULT_CATEGORIES = [
    "Comida",
    "Transporte",
    "Mascotas",
    "Salud",
    "Cuentas",
    "Compras",
    "Ocio",
    "Educación",
    "Otros",
]


def _ensure_db_dir() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Return a sqlite3 connection with row_factory set to Row."""
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db() -> None:
    """Create tables and seed default categories if needed."""
    _ensure_db_dir()
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT    NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                amount         REAL    NOT NULL,
                description    TEXT    NOT NULL,
                date           TEXT    NOT NULL,
                category       TEXT    NOT NULL,
                payment_method TEXT    NOT NULL,
                notes          TEXT    DEFAULT ''
            );
            """
        )

        # Seed default categories only when the table is empty
        count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                [(c,) for c in _DEFAULT_CATEGORIES],
            )
        conn.commit()
