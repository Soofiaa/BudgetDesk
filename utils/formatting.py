"""
formatting.py
Funciones utilitarias para formato de moneda CLP y fechas.
"""
from datetime import datetime


def format_clp(amount: float) -> str:
    """Formatea un número como Peso Chileno: $1.234.567"""
    return "$" + f"{int(round(amount)):,}".replace(",", ".")


def date_to_display(date_str: str) -> str:
    """Convierte YYYY-MM-DD (formato BD) a DD/MM/YYYY (formato visual)."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, AttributeError):
        return date_str


def date_to_db(date_str: str) -> str:
    """Convierte DD/MM/YYYY (formato visual) a YYYY-MM-DD (formato BD)."""
    try:
        return datetime.strptime(date_str.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return date_str
