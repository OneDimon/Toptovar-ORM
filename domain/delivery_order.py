from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class DeliveryStatus(str, Enum):
    NEW         = "new"
    TAKEN       = "taken"
    IN_PROGRESS = "in_progress"
    DONE        = "done"
    CANCELLED   = "cancelled"


@dataclass
class DeliveryOrder:
    """Доменная модель заявки на отгрузку."""
    id: int
    buyer_id: int
    description: str
    address_from: str
    address_to: str
    status: DeliveryStatus = DeliveryStatus.NEW
    loader_id: Optional[int] = None
    seller_id: Optional[int] = None
    photo_done: Optional[str] = None
    comment_done: Optional[str] = None
    created_at: Optional[datetime] = None
    taken_at: Optional[datetime] = None
    in_progress_at: Optional[datetime] = None
    done_at: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        return self.status == DeliveryStatus.NEW

    @property
    def is_active(self) -> bool:
        return self.status in (DeliveryStatus.TAKEN, DeliveryStatus.IN_PROGRESS)
