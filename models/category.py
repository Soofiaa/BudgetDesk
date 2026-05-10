from dataclasses import dataclass


@dataclass
class Category:
    name: str
    id: int | None = None
