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
   DB_HOST=localhost
   DB_USER=postgres
   DB_PASSWORD=...
   DB_NAME=...

4. Применить миграции для основной бд
   poetry run alembic upgrade head
   Применить миграции для тестов 
   poetry run alembic -x database=test upgrade head

5. Запустить
   poetry run uvicorn bookingroom.main:app --reload

## Документация API
После запуска: http://127.0.0.1:8000/docs