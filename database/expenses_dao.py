"""
expenses_dao.py
Data Access Object for the expenses table.
"""
from __future__ import annotations

from typing import Optional

from database.db_manager import get_connection
from models.expense import Expense


def insert(expense: Expense) -> int:
    """Insert a new expense and return its new id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (amount, description, date, category, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                expense.amount,
                expense.description,
                expense.date,
                expense.category,
                expense.payment_method,
                expense.notes,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def update(expense: Expense) -> None:
    """Update an existing expense by id."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE expenses
            SET amount=?, description=?, date=?, category=?, payment_method=?, notes=?
            WHERE id=?
            """,
            (
                expense.amount,
                expense.description,
                expense.date,
                expense.category,
                expense.payment_method,
                expense.notes,
                expense.id,
            ),
        )
        conn.commit()


def delete(expense_id: int) -> None:
    """Delete an expense by id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()


def fetch_all() -> list[Expense]:
    """Return all expenses ordered by date descending."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC"
        ).fetchall()
    return [_row_to_expense(r) for r in rows]


def fetch_filtered(
    month: Optional[str] = None,       # "YYYY-MM"
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
) -> list[Expense]:
    """
    Return expenses matching the given filters.
    Pass None to skip a filter.
    """
    query = "SELECT * FROM expenses WHERE 1=1"
    params: list = []

    if month:
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(month)
    if category:
        query += " AND category = ?"
        params.append(category)
    if payment_method:
        query += " AND payment_method = ?"
        params.append(payment_method)

    query += " ORDER BY date DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_row_to_expense(r) for r in rows]


# ── helpers ──────────────────────────────────────────────────────────────────

def _row_to_expense(row: object) -> Expense:
    return Expense(
        id=row["id"],
        amount=row["amount"],
        description=row["description"],
        date=row["date"],
        category=row["category"],
        payment_method=row["payment_method"],
        notes=row["notes"] or "",
    )
