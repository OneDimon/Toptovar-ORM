"""In-memory реализация IUserRepository для тестов.

Позволяет тестировать handlers БЕЗ запущенной базы данных.
Просто подменяешь UserPostgresRepository на UserInMemoryRepository
в тестах — и всё работает, потому что интерфейс одинаковый.
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from domain.user import User


class UserInMemoryRepository:
    def __init__(self):
        self._storage: Dict[int, User] = {}

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return self._storage.get(user_id)

    async def exists(self, user_id: int) -> bool:
        return user_id in self._storage

    async def create(self, user_id: int, name: str) -> User:
        user = User(user_id=user_id, name=name)
        self._storage[user_id] = user
        return user

    async def update(self, user: User) -> User:
        self._storage[user.user_id] = user
        return user

    async def delete(self, user_id: int) -> bool:
        if user_id in self._storage:
            del self._storage[user_id]
            return True
        return False

    async def set_city(self, user_id: int, city: str) -> None:
        if user_id in self._storage:
            self._storage[user_id].city = city

    async def set_organization(self, user_id: int, organization: str) -> None:
        if user_id in self._storage:
            self._storage[user_id].organization = organization

    async def set_offerta(self, user_id: int) -> None:
        if user_id in self._storage:
            self._storage[user_id].offerta = True

    async def set_phone(self, user_id: int, phone: str) -> None:
        if user_id in self._storage:
            self._storage[user_id].phone = phone

    async def activate_subscription(self, user_id: int, days: int) -> None:
        if user_id in self._storage:
            self._storage[user_id].subscription = True
            self._storage[user_id].date_end_subscription = (
                datetime.now() + timedelta(days=days)
            )

    async def get_all(self) -> List[User]:
        return list(self._storage.values())
