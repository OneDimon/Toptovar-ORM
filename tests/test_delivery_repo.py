"""Тесты DeliveryOrderRepository — запускаются без реальной БД."""
import pytest
from repositories.inmemory.delivery_order import DeliveryOrderInMemoryRepository
from domain.delivery_order import DeliveryStatus


@pytest.fixture
def repo():
    return DeliveryOrderInMemoryRepository()


@pytest.mark.asyncio
async def test_create_order(repo):
    order = await repo.create(
        buyer_id=1,
        description="Коробки с товаром",
        address_from="Ряд 5, место 12",
        address_to="Склад B"
    )
    assert order.id == 1
    assert order.status == DeliveryStatus.NEW
    assert order.is_open is True


@pytest.mark.asyncio
async def test_take_order(repo):
    order = await repo.create(1, "Груз", "Откуда", "Куда")
    success = await repo.take(order.id, loader_id=42)
    assert success is True
    updated = await repo.get_by_id(order.id)
    assert updated.status == DeliveryStatus.TAKEN
    assert updated.loader_id == 42


@pytest.mark.asyncio
async def test_take_already_taken_order_fails(repo):
    order = await repo.create(1, "Груз", "Откуда", "Куда")
    await repo.take(order.id, loader_id=42)
    second = await repo.take(order.id, loader_id=99)
    assert second is False


@pytest.mark.asyncio
async def test_complete_order(repo):
    order = await repo.create(1, "Груз", "Откуда", "Куда")
    await repo.take(order.id, loader_id=42)
    await repo.start(order.id, loader_id=42)
    done = await repo.complete(order.id, loader_id=42, photo="photo_id", comment="Всё OK")
    assert done is not None
    assert done.status == DeliveryStatus.DONE
    assert done.photo_done == "photo_id"


@pytest.mark.asyncio
async def test_cancel_order(repo):
    order = await repo.create(buyer_id=5, description="X", address_from="A", address_to="B")
    cancelled = await repo.cancel(order.id, buyer_id=5)
    assert cancelled is True
    updated = await repo.get_by_id(order.id)
    assert updated.status == DeliveryStatus.CANCELLED


@pytest.mark.asyncio
async def test_get_open_orders(repo):
    await repo.create(1, "Груз 1", "A", "B")
    o2 = await repo.create(2, "Груз 2", "C", "D")
    await repo.take(o2.id, loader_id=10)
    open_orders = await repo.get_open_orders()
    assert len(open_orders) == 1
