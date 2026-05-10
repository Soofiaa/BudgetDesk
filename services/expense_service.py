"""
expense_service.py
Business logic: validation and aggregation using Pandas.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd

from database import fetch_filtered_expenses
from models.expense import Expense

PAYMENT_METHODS = ["debit", "bank_transfer", "credit_card"]
PAYMENT_LABELS = {
    "debit": "Débito",
    "bank_transfer": "Transferencia Bancaria",
    "credit_card": "Tarjeta de Crédito",
}
# Nombres en español para los dropdowns de la interfaz
PAYMENT_DISPLAY_NAMES = ["Débito", "Transferencia Bancaria", "Tarjeta de Crédito"]
PAYMENT_DISPLAY_TO_METHOD = dict(zip(PAYMENT_DISPLAY_NAMES, PAYMENT_METHODS))
PAYMENT_METHOD_TO_DISPLAY = {v: k for k, v in PAYMENT_DISPLAY_TO_METHOD.items()}


# ── Validation ────────────────────────────────────────────────────────────────

def validate_expense(
    amount_str: str,
    description: str,
    date: str,
    category: str,
    payment_method: str,
) -> tuple[bool, str]:
    """
    Validate raw form inputs.
    Returns (is_valid, error_message). error_message is "" when valid.
    """
    if not amount_str.strip():
        return False, "El monto es requerido."
    try:
        amount = float(amount_str.replace(",", "."))
        if amount <= 0:
            return False, "El monto debe ser mayor a cero."
    except ValueError:
        return False, "El monto debe ser un número válido."

    if not description.strip():
        return False, "La descripción es requerida."
    if not date.strip():
        return False, "La fecha es requerida."
    try:
        datetime.strptime(date.strip(), "%d/%m/%Y")
    except ValueError:
        return False, "La fecha debe tener el formato DD/MM/AAAA (ej. 31/01/2025)."
    if not category.strip():
        return False, "La categoría es requerida."
    if payment_method not in PAYMENT_METHODS:
        return False, "Método de pago inválido."

    return True, ""


# ── Aggregation ───────────────────────────────────────────────────────────────

def get_monthly_summary(
    month: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
) -> dict:
    """
    Return a summary dict for the given filters:
    {
        "total": float,
        "by_payment": {"debit": float, "bank_transfer": float, "credit_card": float},
        "by_category": {category_name: float, ...},
        "count": int,
    }
    """
    expenses = fetch_filtered_expenses(month=month, category=category, payment_method=payment_method)

    if not expenses:
        return {
            "total": 0.0,
            "by_payment": {m: 0.0 for m in PAYMENT_METHODS},
            "by_category": {},
            "count": 0,
        }

    df = _to_dataframe(expenses)

    by_payment = (
        df.groupby("payment_method")["amount"]
        .sum()
        .reindex(PAYMENT_METHODS, fill_value=0.0)
        .to_dict()
    )

    by_category = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    return {
        "total": float(df["amount"].sum()),
        "by_payment": by_payment,
        "by_category": by_category,
        "count": len(df),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_dataframe(expenses: list[Expense]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "id": e.id,
                "amount": e.amount,
                "description": e.description,
                "date": e.date,
                "category": e.category,
                "payment_method": e.payment_method,
                "notes": e.notes,
            }
            for e in expenses
        ]
    )
