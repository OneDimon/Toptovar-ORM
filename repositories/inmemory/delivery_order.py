from datetime import datetime
from typing import Optional, List, Dict
from domain.delivery_order import DeliveryOrder, DeliveryStatus


class DeliveryOrderInMemoryRepository:
    def __init__(self):
        self._storage: Dict[int, DeliveryOrder] = {}
        self._next_id: int = 1

    async def get_by_id(self, order_id: int) -> Optional[DeliveryOrder]:
        return self._storage.get(order_id)

    async def create(self, buyer_id: int, description: str,
                     address_from: str, address_to: str) -> DeliveryOrder:
        order = DeliveryOrder(
            id=self._next_id,
            buyer_id=buyer_id,
            description=description,
            address_from=address_from,
            address_to=address_to,
            created_at=datetime.now(),
        )
        self._storage[self._next_id] = order
        self._next_id += 1
        return order

    async def get_open_orders(self) -> List[DeliveryOrder]:
        return [o for o in self._storage.values() if o.is_open]

    async def get_by_buyer(self, buyer_id: int) -> List[DeliveryOrder]:
        return [o for o in self._storage.values() if o.buyer_id == buyer_id]

    async def get_by_loader(self, loader_id: int) -> List[DeliveryOrder]:
        return [o for o in self._storage.values() if o.loader_id == loader_id]

    async def take(self, order_id: int, loader_id: int) -> bool:
        order = self._storage.get(order_id)
        if not order or not order.is_open:
            return False
        order.status = DeliveryStatus.TAKEN
        order.loader_id = loader_id
        order.taken_at = datetime.now()
        return True

    async def start(self, order_id: int, loader_id: int) -> bool:
        order = self._storage.get(order_id)
        if not order or order.loader_id != loader_id or order.status != DeliveryStatus.TAKEN:
            return False
        order.status = DeliveryStatus.IN_PROGRESS
        order.in_progress_at = datetime.now()
        return True

    async def complete(self, order_id: int, loader_id: int,
                       photo: str, comment: str) -> Optional[DeliveryOrder]:
        order = self._storage.get(order_id)
        if not order or order.loader_id != loader_id or order.status != DeliveryStatus.IN_PROGRESS:
            return None
        order.status = DeliveryStatus.DONE
        order.photo_done = photo
        order.comment_done = comment
        order.done_at = datetime.now()
        return order

    async def cancel(self, order_id: int, buyer_id: int) -> bool:
        order = self._storage.get(order_id)
        if not order or order.buyer_id != buyer_id or not order.is_open:
            return False
        order.status = DeliveryStatus.CANCELLED
        return True
