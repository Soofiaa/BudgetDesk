"""
categories_dao.py
Data Access Object for the categories table.
"""
from __future__ import annotations

from database.db_manager import get_connection
from models.category import Category


def fetch_all() -> list[Category]:
    """Return all categories ordered alphabetically."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM categories ORDER BY name ASC"
        ).fetchall()
    return [Category(id=r["id"], name=r["name"]) for r in rows]


def fetch_names() -> list[str]:
    """Return category names only (useful for dropdowns)."""
    return [c.name for c in fetch_all()]


def insert(name: str) -> Category:
    """Insert a new category and return it. Raises ValueError if name exists."""
    name = name.strip()
    if not name:
        raise ValueError("El nombre de la categoría no puede estar vacío.")
    with get_connection() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO categories (name) VALUES (?)", (name,)
            )
            conn.commit()
            return Category(id=cursor.lastrowid, name=name)
        except Exception as exc:
            raise ValueError(f"La categoría '{name}' ya existe.") from exc


def delete(category_id: int) -> None:
    """Delete a category by id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM categories WHERE id=?", (category_id,))
        conn.commit()
