# Сервис объявлений (FastAPI + PostgreSQL)

## Стек технологий

- **Backend**: 
  - Python 3.11
  - FastAPI
  - SQLAlchemy
  - Uvicorn (ASGI сервер)

- **База данных**:
  - PostgreSQL 15+
  - Asyncpg (Для работы с PostgreSQL)

- **Аутентификация**:
  - JWT
  - OAuth2

## Требования

- Docker 20.10+
- Docker Compose 2.20+
- Python 3.11

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/MaXIDoGG/ad_placement_service
cd ad_placement_service
```

### 2. Настройка окружения
Создайте файл .env в корне проекта (пример есть в файле [.env.template](https://github.com/MaXIDoGG/ad_placement_service/blob/main/.env.template))

### 3. Запуск
```bash
docker-compose up --build
```

Сервис будет доступен по адресу:
http://localhost:8000

Документация API:
http://localhost:8000/docs
