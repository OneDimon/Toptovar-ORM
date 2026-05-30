# Toptovar-ORM

Архитектурный шаблон для [Toptovarbot](https://github.com/OneDimon/Toptovarbot) — реализация **Repository Pattern** с использованием:

- **SQLAlchemy 2.0 async** + **asyncpg** — полностью неблокирующая работа с PostgreSQL
- **Alembic** — автогенерация миграций из моделей
- **Domain models** (dataclasses) — типизированные объекты вместо сырых кортежей
- **Protocol-based interfaces** — абстракция без зависимости от конкретной ORM

## Структура

```
Toptovar-ORM/
├── domain/              # Доменные модели (@dataclass)
│   ├── user.py
│   ├── product.py
│   ├── delivery_order.py
│   ├── referral.py
│   └── history_transaction.py
│
├── repositories/
│   ├── interfaces/      # Протоколы (ABC) — контракт без реализации
│   │   ├── user.py
│   │   ├── delivery_order.py
│   │   ├── product.py
│   │   └── referral.py
│   ├── postgres/        # Реализация для PostgreSQL (asyncpg + SQLAlchemy)
│   │   ├── user.py
│   │   ├── delivery_order.py
│   │   ├── product.py
│   │   └── referral.py
│   └── inmemory/        # Фейковая реализация для тестов
│       ├── user.py
│       └── delivery_order.py
│
├── database/
│   ├── engine.py        # Один async engine + sessionmaker
│   └── models.py        # SQLAlchemy ORM-модели (таблицы)
│
├── migrations/          # Alembic
│   ├── env.py
│   └── versions/
│
├── tests/               # Тесты без реальной БД (inmemory)
│   ├── test_user_repo.py
│   └── test_delivery_repo.py
│
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

## Главная идея

```python
# Было (в handlers):
user = await UsersDatabase.get_user(user_id)
if user[3] == True:  # что такое [3]? только бог знает

# Стало:
user = await self.user_repo.get_by_id(user_id)
if user.subscription:  # читаемо, типизировано, автодополнение
```

## Как использовать

```bash
pip install -r requirements.txt
cp .env.example .env  # заполнить DB_URL
alembic upgrade head  # применить миграции
```

## Замена БД

Чтобы переключиться с PostgreSQL на другую БД — меняется **только** `database/engine.py` и `repositories/postgres/`.
Handlers и бизнес-логика не трогаются вообще.
