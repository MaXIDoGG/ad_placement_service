# Сервис объявлений (FastAPI + PostgreSQL)

## Стек технологий

- **Backend**: 
  - Python 3.11
  - FastAPI 0.109+
  - SQLAlchemy 2.0+ (с async поддержкой)
  - Uvicorn (ASGI сервер)

- **База данных**:
  - PostgreSQL 15+
  - Asyncpg (драйвер для работы с PostgreSQL)

- **Аутентификация**:
  - JWT (JSON Web Tokens)
  - OAuth2 с Password flow

## Требования

- Docker 20.10+
- Docker Compose 2.20+
- Python 3.11 (для локальной разработки)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/ads-service.git
cd ads-service