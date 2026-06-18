# BookingRoom API

## Технологии
FastAPI, PostgreSQL, SQLAlchemy, Alembic, Poetry

## Установка и запуск

1. Клонировать и зайти в проект
   git clone <репозиторий>
   cd bookingroom

2. Установить зависимости
   poetry install

3. Создать .env по образцу .env.example и заполнить
   BD_HOST=localhost
   BD_USER=postgres
   BD_PASSWORD=...
   BD_NAME=...

4. Применить миграции
   poetry run alembic upgrade head

5. Запустить
   poetry run uvicorn bookingroom.main:app --reload

## Документация API
После запуска: http://127.0.0.1:8000/docs