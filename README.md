<div align="center">

# 🤖 Feedback Bot

**Бот обратной связи для网站 — получайте сообщения с сайта прямо в Telegram**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="README_EN.md">🇬🇧 English version</a>
</p>

</div>

---

## 📖 Описание проекта

**Feedback Bot** — это backend-API сервис, который принимает контактные формы с сайта и пересылает их в Telegram в виде отформатированного сообщения.

```
👤 Пользователь  →  🌐 Сайт  →  ⚡ FastAPI  →  🤖 Telegram
  (форма)          (фронтенд)    (этот бот)     (ваш чат)
```

**Использование:**
- Форма обратной связи на сайте ([dushafullstack.ru](https://dushafullstack.ru))
- Сообщения с лендингов и портфолио
- Обратная связь от клиентов
- Уведомления о заявках

---

## 📸 Пример сообщения в Telegram

<div align="center">
  <img src="img/telegram_msg.png" alt="Пример сообщения в Telegram" width="400"/>
</div>

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 📨 Приём форм | `POST /api/contact` — принимает JSON с данными формы |
| ✅ Валидация | Проверка имени, сообщения (мин. 10 символов), формата email |
| 🤖 Отправка в Telegram | Форматированное Markdown-сообщение с эмодзи |
| 🔒 Прокси-поддержка | SOCKS4/5 и HTTP(S) прокси для обхода блокировок |
| 🩺 Healthcheck | `GET /health` — проверка работоспособности сервиса |
| 🐳 Docker | Готовый Dockerfile и docker-compose |
| 🌐 CORS | Настраиваемые разрешённые origins |

---

## 🏗 Архитектура

```
feedback-bot/
├── src/
│   ├── main.py                # Точка входа, FastAPI-приложение
│   ├── config.py              # Конфигурация (pydantic-settings)
│   ├── telegram_session.py    # Прокси-сессия для Telegram API
│   ├── gunicorn.conf.py       # Конфигурация Gunicorn (prod)
│   ├── api/
│   │   └── routes.py          # REST API endpoints
│   ├── models/
│   │   └── schemas.py         # Pydantic модели данных
│   ├── services/
│   │   └── telegram_service.py # Сервис отправки в Telegram
│   └── utils/
│       └── validators.py      # Валидация данных
├── Docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env.example
└── LICENSE (MIT)
```

---

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/Dusha01/feedback-bot.git
cd feedback-bot
```

### 2. Настройка окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` — введите реальные значения:

```env
BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
CHAT_ID="-1001234567890"
CORS_ORIGINS=["https://dushafullstack.ru"]
APP_HOST="0.0.0.0"
APP_PORT=8000
APP_DEBUG=false
TELEGRAM_PROXY_URL=socks5://user:pass@host:port
```

### 3. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### 4. Запуск

**Development:**
```bash
python src/main.py
# или
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Production (Gunicorn):**
```bash
gunicorn src.main:app -c src/gunicorn.conf.py
```

**Docker:**
```bash
cd Docker
docker-compose up --build
```

---

## 📡 API Endpoints

### `GET /` — Приветствие

```json
{
  "message": "Contact Form API is running"
}
```

---

### `GET /health` — Healthcheck

```json
{
  "status": "healthy"
}
```

---

### `POST /api/contact` — Отправка контактной формы

**Headers:**
```
Content-Type: application/json
```

**Request Body:**

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| `name` | `string` | ✅ | Имя пользователя |
| `phone` | `string` | ✅ | Номер телефона |
| `email` | `string` | ✅ | Email (валидный формат) |
| `subject` | `string` | ✅ | Тема обращения |
| `message` | `string` | ✅ | Текст сообщения (мин. 10 символов) |

**Пример запроса (curl):**

```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Иванов",
    "phone": "+7 (999) 123-45-67",
    "email": "ivan@example.com",
    "subject": "Сотрудничество",
    "message": "Здравствуйте! Хотел бы обсудить возможность сотрудничества."
  }'
```

**Успешный ответ (200):**

```json
{
  "status": "success",
  "message": "Form submitted successfully",
  "telegram_sent": true
}
```

**Ошибки:**

| Код | Описание | Пример |
|-----|----------|--------|
| `400` | Ошибка валидации | `"Имя обязательно для заполнения"`, `"Сообщение должно содержать не менее 10 символов"` |
| `422` | Невалидный JSON | Отсутствует обязательное поле / неверный тип |
| `500` | Внутренняя ошибка сервера | `"Internal server error"` |

---

## 📋 Модели данных

### `ContactForm` — Входная модель

```python
class ContactForm(BaseModel):
    name: str         # Имя
    phone: str        # Телефон
    email: EmailStr   # Email (с валидацией формата)
    subject: str      # Тема
    message: str      # Сообщение (мин. 10 символов)
```

### `ContactResponse` — Ответ API

```python
class ContactResponse(BaseModel):
    status: str       # Статус ("success")
    message: str      # Описание результата
    telegram_sent: bool  # Доставлено ли в Telegram
```

---

## ⚙️ Конфигурация

Все переменные задаются через `.env` файл:

| Переменная | Тип | Обязательно | По умолчанию | Описание |
|-----------|-----|-------------|-------------|----------|
| `BOT_TOKEN` | `string` | ✅ | — | Токен Telegram-бота (от [@BotFather](https://t.me/BotFather)) |
| `CHAT_ID` | `string` | ✅ | — | ID чата/группы для получения сообщений |
| `CORS_ORIGINS` | `string[]` | ✅ | `["*"]` | Разрешённые origins для CORS |
| `APP_HOST` | `string` | ✅ | `0.0.0.0` | Хост для прослушивания |
| `APP_PORT` | `integer` | ✅ | `8000` | Порт сервера |
| `APP_DEBUG` | `boolean` | ✅ | `false` | Режим отладки |
| `TELEGRAM_PROXY_URL` | `string` | ❌ | `None` | Прокси для Telegram API |

### 🔒 Прокси

Если Telegram API заблокирован, настройте прокси:

```env
# SOCKS5
TELEGRAM_PROXY_URL=socks5://user:pass@host:port

# SOCKS4
TELEGRAM_PROXY_URL=socks4://user:pass@host:port

# HTTP(S)
TELEGRAM_PROXY_URL=http://user:pass@host:port
```

### 🌐 CORS

Для работы с фронтендом укажите его домен:

```env
CORS_ORIGINS=["https://dushafullstack.ru", "http://localhost:3000"]
```

Для разрешения всех источников (только для разработки!):

```env
CORS_ORIGINS=["*"]
```

---

## 🐳 Docker

### Сборка и запуск

```bash
cd Docker
docker-compose up --build -d
```

### Остановка

```bash
docker-compose down
```

### Healthcheck

Контейнер автоматически проверяет работоспособность каждые 30 секунд:

```bash
curl http://localhost:8080/health
```

---

## 🔧 Технологии

| Компонент | Технология | Версия |
|-----------|-----------|--------|
| Язык | Python | 3.12 |
| Веб-фреймворк | FastAPI | 0.136.1 |
| Валидация | Pydantic | 2.13.4 |
| Telegram | aiogram | 3.28.2 |
| Прокси | aiohttp-socks | 0.11.0 |
| ASGI-сервер | Uvicorn | 0.46.0 |
| Prod-сервер | Gunicorn | — |
| Контейнеризация | Docker | — |

---

## 📜 Лицензия

MIT License — см. [LICENSE](LICENSE).

---

<div align="center">

**Сделано с ❤️ для [Dusha Fullstack](https://dushafullstack.ru)**

</div>
