"""Тесты UserRepository — запускаются без реальной БД."""
import pytest
from repositories.inmemory.user import UserInMemoryRepository


@pytest.fixture
def repo():
    return UserInMemoryRepository()


@pytest.mark.asyncio
async def test_create_user(repo):
    user = await repo.create(123456, "Иван")
    assert user.user_id == 123456
    assert user.name == "Иван"
    assert user.subscription is False


@pytest.mark.asyncio
async def test_get_by_id(repo):
    await repo.create(111, "Мария")
    user = await repo.get_by_id(111)
    assert user is not None
    assert user.name == "Мария"


@pytest.mark.asyncio
async def test_get_nonexistent_returns_none(repo):
    user = await repo.get_by_id(999)
    assert user is None


@pytest.mark.asyncio
async def test_activate_subscription(repo):
    await repo.create(222, "Пётр")
    await repo.activate_subscription(222, days=30)
    user = await repo.get_by_id(222)
    assert user.subscription is True
    assert user.has_active_subscription is True


@pytest.mark.asyncio
async def test_set_city(repo):
    await repo.create(333, "Анна")
    await repo.set_city(333, "Москва")
    user = await repo.get_by_id(333)
    assert user.city == "Москва"


@pytest.mark.asyncio
async def test_delete_user(repo):
    await repo.create(444, "Алексей")
    deleted = await repo.delete(444)
    assert deleted is True
    assert await repo.get_by_id(444) is None
