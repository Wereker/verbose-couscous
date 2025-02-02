# Carwash API

Carwash API — это RESTful API для управления онлайн-записью и процессами автомойки. Система позволяет пользователям записываться на услуги, а администраторам управлять бронированиями и клиентами.

## 🚀 Стек технологий

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose
- **Фоновая обработка задач**: Celery, Redis

## 📌 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/carwash-api.git
cd carwash-api
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:

```
APP_CONFIG__DB__URL=postgresql+asyncpg://app:app@pg:5432/app

APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET=your_reset_password_token_secret
APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET=your_verification_token_secret

APP_CONFIG__AUTH__SECRET_KEY=your_secret_key
APP_CONFIG__AUTH__REFRESH_SECRET_KEY=your_refresh_secret_key
APP_CONFIG__AUTH__ALGORITHM=HS256
APP_CONFIG__AUTH__ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_CONFIG__AUTH__REFRESH_TOKEN_EXPIRE_MINUTES=10080


APP_CONFIG__REDIS__HOST=redis
APP_CONFIG__REDIS__PORT=6379
APP_CONFIG__REDIS__EXPIRE_SECONDS=3600


APP_CONFIG__CELERY__SMTP_HOSTNAME=your_smtp_hostname
APP_CONFIG__CELERY__SMTP_PORT=your_smtp_port
APP_CONFIG__CELERY__EMAIL_SENDER=your_email_sender
APP_CONFIG__CELERY__EMAIL_USERNAME=your_email_username
APP_CONFIG__CELERY__EMAIL_PASSWORD=your_email_password
```

### 3. Запуск проекта с Docker

```bash
docker-compose up --build
```

### 4. Применение миграций

После запуска контейнеров, выполните:

```bash
docker-compose exec carwash-api alembic upgrade head
```

### 5. Добавление тестовых данных

Запустите команду:

```bash
docker-compose exec carwash-api python create_data_app.py
```

## 📖 Использование API

После запуска API доступно по адресу: `http://localhost:8000`

### 🔹 Документация API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🛠 Основные эндпоинты

| Метод  | URL                                  | Описание                       | Доступ             |
| ------ | ------------------------------------ | ------------------------------ | ------------------ |
| POST   | `/api/v1/orders/`                    | Создание нового заказа         | Для клиента        |
| PATCH  | `/api/v1/orders/{order_id}/assign`   | Добавить к заказу рабочего     | Для администратора |
| PATCH  | `/api/v1/orders/{order_id}/services` | Добавить новые услуги к заказу | Для клиента        |
| PATCH  | `/api/v1/orders/{order_id}/complete` | Поменять статус заказа         | Для администратора |

## 📌 Дополнительно

- Если необходимо остановить контейнеры:
  ```bash
  docker-compose down
  ```

---

✨ **Carwash API** создан для удобного управления записями на автомойку!

