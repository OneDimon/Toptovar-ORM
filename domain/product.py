from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Доменная модель товара продавца."""
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    category_two: Optional[str] = None
    category_three: Optional[str] = None
    price: Optional[float] = None
    photo: Optional[str] = None
    date_publication: Optional[datetime] = None
    available: bool = True
