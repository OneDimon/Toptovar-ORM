"""SQLAlchemy ORM-модели — описание таблиц.

Это технический слой (как устроена БД).
Доменные модели в domain/ — это бизнес-слой (как устроена логика).
Репозиторий преобразует одно в другое.
"""
from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey,
    Numeric, String, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base
from datetime import datetime
from typing import Optional


class UserORM(Base):
    __tablename__ = "users"

    user_id:                Mapped[int]            = mapped_column(BigInteger, primary_key=True)
    name:                   Mapped[str]            = mapped_column(String(255))
    city:                   Mapped[Optional[str]]  = mapped_column(String(255))
    subscription:           Mapped[bool]           = mapped_column(Boolean, default=False)
    date_end_subscription:  Mapped[Optional[datetime]] = mapped_column(DateTime)
    organization:           Mapped[Optional[str]]  = mapped_column(String(500))
    offerta:                Mapped[bool]           = mapped_column(Boolean, default=False)
    phone:                  Mapped[Optional[str]]  = mapped_column(String(50))
    rights:                 Mapped[Optional[str]]  = mapped_column(String(50))


class ProductORM(Base):
    __tablename__ = "product"

    id:               Mapped[int]            = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id:          Mapped[int]            = mapped_column(BigInteger, ForeignKey("users.user_id"))
    name:             Mapped[str]            = mapped_column(String(500))
    description:      Mapped[Optional[str]]  = mapped_column(Text)
    category:         Mapped[Optional[str]]  = mapped_column(String(255))
    category_two:     Mapped[Optional[str]]  = mapped_column(String(255))
    category_three:   Mapped[Optional[str]]  = mapped_column(String(255))
    price:            Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    photo:            Mapped[Optional[str]]  = mapped_column(Text)
    date_publication: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    available:        Mapped[bool]           = mapped_column(Boolean, default=True)


class DeliveryOrderORM(Base):
    __tablename__ = "delivery_order"

    id:             Mapped[int]            = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    buyer_id:       Mapped[int]            = mapped_column(BigInteger, ForeignKey("users.user_id"))
    loader_id:      Mapped[Optional[int]]  = mapped_column(BigInteger, ForeignKey("users.user_id"))
    seller_id:      Mapped[Optional[int]]  = mapped_column(BigInteger, ForeignKey("users.user_id"))
    description:    Mapped[str]            = mapped_column(Text)
    address_from:   Mapped[str]            = mapped_column(String(500))
    address_to:     Mapped[str]            = mapped_column(String(500))
    status:         Mapped[str]            = mapped_column(String(50), default="new")
    photo_done:     Mapped[Optional[str]]  = mapped_column(Text)
    comment_done:   Mapped[Optional[str]]  = mapped_column(Text)
    created_at:     Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    taken_at:       Mapped[Optional[datetime]] = mapped_column(DateTime)
    in_progress_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    done_at:        Mapped[Optional[datetime]] = mapped_column(DateTime)


class ReferralORM(Base):
    __tablename__ = "referral"

    id:               Mapped[int]            = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id:          Mapped[int]            = mapped_column(BigInteger, ForeignKey("users.user_id"), unique=True)
    referrer_id:      Mapped[int]            = mapped_column(BigInteger, ForeignKey("users.user_id"))
    link:             Mapped[str]            = mapped_column(String(1000))
    points:           Mapped[Optional[int]]  = mapped_column(BigInteger, default=0)
    group_points:     Mapped[Optional[int]]  = mapped_column(BigInteger, default=0)
    sop:              Mapped[Optional[int]]  = mapped_column(BigInteger, default=0)
    status:           Mapped[Optional[str]]  = mapped_column(String(100))
    last_status:      Mapped[Optional[str]]  = mapped_column(String(100))
    balance:          Mapped[Optional[int]]  = mapped_column(BigInteger, default=0)
    potential_status: Mapped[Optional[str]]  = mapped_column(String(100))


class HistoryTransactionORM(Base):
    __tablename__ = "history_transaction"

    id:         Mapped[int]   = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id:    Mapped[int]   = mapped_column(BigInteger, ForeignKey("users.user_id"))
    amount:     Mapped[float] = mapped_column(Numeric(10, 2))
    amount_rub: Mapped[float] = mapped_column(Numeric(10, 2))
    type:       Mapped[str]   = mapped_column(String(100))
    date_time:  Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
