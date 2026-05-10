from dataclasses import dataclass, field


@dataclass
class Expense:
    amount: float
    description: str
    date: str          # YYYY-MM-DD
    category: str
    payment_method: str  # 'debit' | 'bank_transfer' | 'credit_card'
    notes: str = ""
    id: int | None = None
