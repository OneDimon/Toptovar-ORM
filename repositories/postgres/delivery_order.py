from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.delivery_order import DeliveryOrder, DeliveryStatus
from database.models import DeliveryOrderORM


def _to_domain(row: DeliveryOrderORM) -> DeliveryOrder:
    return DeliveryOrder(
        id=row.id,
        buyer_id=row.buyer_id,
        loader_id=row.loader_id,
        seller_id=row.seller_id,
        description=row.description,
        address_from=row.address_from,
        address_to=row.address_to,
        status=DeliveryStatus(row.status),
        photo_done=row.photo_done,
        comment_done=row.comment_done,
        created_at=row.created_at,
        taken_at=row.taken_at,
        in_progress_at=row.in_progress_at,
        done_at=row.done_at,
    )


class DeliveryOrderPostgresRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, order_id: int) -> Optional[DeliveryOrder]:
        row = await self._session.get(DeliveryOrderORM, order_id)
        return _to_domain(row) if row else None

    async def create(self, buyer_id: int, description: str,
                     address_from: str, address_to: str) -> DeliveryOrder:
        row = DeliveryOrderORM(
            buyer_id=buyer_id,
            description=description,
            address_from=address_from,
            address_to=address_to,
        )
        self._session.add(row)
        await self._session.flush()
        return _to_domain(row)

    async def get_open_orders(self) -> List[DeliveryOrder]:
        result = await self._session.execute(
            select(DeliveryOrderORM)
            .where(DeliveryOrderORM.status == DeliveryStatus.NEW.value)
            .order_by(DeliveryOrderORM.created_at.desc())
        )
        return [_to_domain(r) for r in result.scalars().all()]

    async def get_by_buyer(self, buyer_id: int) -> List[DeliveryOrder]:
        result = await self._session.execute(
            select(DeliveryOrderORM)
            .where(DeliveryOrderORM.buyer_id == buyer_id)
            .order_by(DeliveryOrderORM.created_at.desc())
        )
        return [_to_domain(r) for r in result.scalars().all()]

    async def get_by_loader(self, loader_id: int) -> List[DeliveryOrder]:
        result = await self._session.execute(
            select(DeliveryOrderORM)
            .where(DeliveryOrderORM.loader_id == loader_id)
            .order_by(DeliveryOrderORM.created_at.desc())
        )
        return [_to_domain(r) for r in result.scalars().all()]

    async def take(self, order_id: int, loader_id: int) -> bool:
        result = await self._session.execute(
            update(DeliveryOrderORM)
            .where(
                DeliveryOrderORM.id == order_id,
                DeliveryOrderORM.status == DeliveryStatus.NEW.value
            )
            .values(
                status=DeliveryStatus.TAKEN.value,
                loader_id=loader_id,
                taken_at=datetime.now()
            )
        )
        return result.rowcount > 0

    async def start(self, order_id: int, loader_id: int) -> bool:
        result = await self._session.execute(
            update(DeliveryOrderORM)
            .where(
                DeliveryOrderORM.id == order_id,
                DeliveryOrderORM.loader_id == loader_id,
                DeliveryOrderORM.status == DeliveryStatus.TAKEN.value
            )
            .values(status=DeliveryStatus.IN_PROGRESS.value, in_progress_at=datetime.now())
        )
        return result.rowcount > 0

    async def complete(self, order_id: int, loader_id: int,
                       photo: str, comment: str) -> Optional[DeliveryOrder]:
        result = await self._session.execute(
            update(DeliveryOrderORM)
            .where(
                DeliveryOrderORM.id == order_id,
                DeliveryOrderORM.loader_id == loader_id,
                DeliveryOrderORM.status == DeliveryStatus.IN_PROGRESS.value
            )
            .values(
                status=DeliveryStatus.DONE.value,
                photo_done=photo,
                comment_done=comment,
                done_at=datetime.now()
            )
            .returning(DeliveryOrderORM)
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def cancel(self, order_id: int, buyer_id: int) -> bool:
        result = await self._session.execute(
            update(DeliveryOrderORM)
            .where(
                DeliveryOrderORM.id == order_id,
                DeliveryOrderORM.buyer_id == buyer_id,
                DeliveryOrderORM.status == DeliveryStatus.NEW.value
            )
            .values(status=DeliveryStatus.CANCELLED.value)
        )
        return result.rowcount > 0
