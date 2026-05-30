from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Доменная модель пользователя.
    
    Не зависит ни от psycopg2, ни от SQLAlchemy, ни от aiogram.
    Хендлеры работают с этим объектом — никаких кортежей user[3].
    """
    user_id: int
    name: str
    city: Optional[str] = None
    subscription: bool = False
    date_end_subscription: Optional[datetime] = None
    organization: Optional[str] = None
    offerta: bool = False
    phone: Optional[str] = None
    rights: Optional[str] = None

    @property
    def has_active_subscription(self) -> bool:
        """Проверяет что подписка активна прямо сейчас."""
        if not self.subscription:
            return False
        if self.date_end_subscription is None:
            return False
        return self.date_end_subscription > datetime.now()

    @property
    def is_admin(self) -> bool:
        return self.rights == "admin"
