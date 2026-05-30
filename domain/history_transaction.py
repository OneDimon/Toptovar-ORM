from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HistoryTransaction:
    """Доменная модель транзакции баланса."""
    id: int
    user_id: int
    amount: float
    amount_rub: float     # amount * 200
    type: str
    date_time: Optional[datetime] = None
