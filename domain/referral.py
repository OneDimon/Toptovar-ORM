from dataclasses import dataclass
from typing import Optional


@dataclass
class Referral:
    """Доменная модель участника реферальной программы."""
    id: int
    user_id: int
    referrer_id: int
    link: str
    points: int = 0
    group_points: int = 0
    sop: int = 0
    status: Optional[str] = None
    last_status: Optional[str] = None
    balance: int = 0
    potential_status: Optional[str] = None
