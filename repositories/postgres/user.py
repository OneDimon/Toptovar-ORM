"""PostgreSQL-реализация IUserRepository.

Если завтра переходим на MongoDB — пишем MongoUserRepository,
реализующий тот же Protocol. Handlers не меняются вообще.
"""
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.user import User
from database.models import UserORM


def _to_domain(row: UserORM) -> User:
    """Конвертирует ORM-объект в доменную модель."""
    return User(
        user_id=row.user_id,
        name=row.name,
        city=row.city,
        subscription=row.subscription,
        date_end_subscription=row.date_end_subscription,
        organization=row.organization,
        offerta=row.offerta,
        phone=row.phone,
        rights=row.rights,
    )


class UserPostgresRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self._session.get(UserORM, user_id)
        return _to_domain(result) if result else None

    async def exists(self, user_id: int) -> bool:
        result = await self._session.get(UserORM, user_id)
        return result is not None

    async def create(self, user_id: int, name: str) -> User:
        row = UserORM(user_id=user_id, name=name)
        self._session.add(row)
        await self._session.flush()
        return _to_domain(row)

    async def update(self, user: User) -> User:
        row = await self._session.get(UserORM, user.user_id)
        if not row:
            raise ValueError(f"User {user.user_id} not found")
        for field in ("name", "city", "subscription", "date_end_subscription",
                      "organization", "offerta", "phone", "rights"):
            setattr(row, field, getattr(user, field))
        await self._session.flush()
        return _to_domain(row)

    async def delete(self, user_id: int) -> bool:
        row = await self._session.get(UserORM, user_id)
        if not row:
            return False
        await self._session.delete(row)
        return True

    async def set_city(self, user_id: int, city: str) -> None:
        await self._session.execute(
            update(UserORM).where(UserORM.user_id == user_id).values(city=city)
        )

    async def set_organization(self, user_id: int, organization: str) -> None:
        await self._session.execute(
            update(UserORM).where(UserORM.user_id == user_id).values(organization=organization)
        )

    async def set_offerta(self, user_id: int) -> None:
        await self._session.execute(
            update(UserORM).where(UserORM.user_id == user_id).values(offerta=True)
        )

    async def set_phone(self, user_id: int, phone: str) -> None:
        await self._session.execute(
            update(UserORM).where(UserORM.user_id == user_id).values(phone=phone)
        )

    async def activate_subscription(self, user_id: int, days: int) -> None:
        end_date = datetime.now() + timedelta(days=days)
        await self._session.execute(
            update(UserORM)
            .where(UserORM.user_id == user_id)
            .values(subscription=True, date_end_subscription=end_date)
        )

    async def get_all(self) -> List[User]:
        result = await self._session.execute(select(UserORM))
        return [_to_domain(row) for row in result.scalars().all()]
