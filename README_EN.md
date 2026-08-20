<div align="center">

# 🤖 Feedback Bot

**Feedback bot for your website — receive messages directly in Telegram**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="README.md">🇷🇺 Русская версия</a>
</p>

</div>

---

## 📖 About the project

**Feedback Bot** is a backend API service that accepts contact forms from a website and forwards them to Telegram as a formatted message.

```
👤 User  →  🌐 Website  →  ⚡ FastAPI  →  🤖 Telegram
 (form)     (frontend)     (this bot)     (your chat)
```

**Use cases:**
- Contact form on a website ([dushafullstack.ru](https://dushafullstack.ru))
- Messages from landing pages and portfolios
- Customer feedback
- Lead notifications

---

## 📸 Telegram message example

<div align="center">
  <img src="img/telegram_msg.png" alt="Telegram message example" width="400"/>
</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📨 Form handling | `POST /api/contact` — accepts JSON with form data |
| ✅ Validation | Name, message (min. 10 chars), email format check |
| 🤖 Telegram delivery | Formatted Markdown message with emojis |
| 🔒 Proxy support | SOCKS4/5 and HTTP(S) proxy for bypassing blocks |
| 🩺 Healthcheck | `GET /health` — service health monitoring |
| 🐳 Docker | Ready-to-use Dockerfile and docker-compose |
| 🌐 CORS | Configurable allowed origins |

---

## 🏗 Architecture

```
feedback-bot/
├── src/
│   ├── main.py                # Entry point, FastAPI application
│   ├── config.py              # Configuration (pydantic-settings)
│   ├── telegram_session.py    # Proxy session for Telegram API
│   ├── gunicorn.conf.py       # Gunicorn config (prod)
│   ├── api/
│   │   └── routes.py          # REST API endpoints
│   ├── models/
│   │   └── schemas.py         # Pydantic data models
│   ├── services/
│   │   └── telegram_service.py # Telegram sending service
│   └── utils/
│       └── validators.py      # Data validation
├── Docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env.example
└── LICENSE (MIT)
```

---

## 🚀 Quick start

### 1. Clone the repo

```bash
git clone https://github.com/Dusha01/feedback-bot.git
cd feedback-bot
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your real values:

```env
BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
CHAT_ID="-1001234567890"
CORS_ORIGINS=["https://dushafullstack.ru"]
APP_HOST="0.0.0.0"
APP_PORT=8000
APP_DEBUG=false
TELEGRAM_PROXY_URL=socks5://user:pass@host:port
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

### 4. Run

**Development:**
```bash
python src/main.py
# or
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

### `GET /` — Welcome

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

### `POST /api/contact` — Submit contact form

**Headers:**
```
Content-Type: application/json
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ | User's name |
| `phone` | `string` | ✅ | Phone number |
| `email` | `string` | ✅ | Email (valid format) |
| `subject` | `string` | ✅ | Subject line |
| `message` | `string` | ✅ | Message text (min. 10 characters) |

**Example request (curl):**

```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+1 (555) 123-4567",
    "email": "john@example.com",
    "subject": "Partnership",
    "message": "Hello! I would like to discuss a potential partnership opportunity."
  }'
```

**Success response (200):**

```json
{
  "status": "success",
  "message": "Form submitted successfully",
  "telegram_sent": true
}
```

**Errors:**

| Code | Description | Example |
|------|-------------|---------|
| `400` | Validation error | `"Имя обязательно для заполнения"`, `"Сообщение должно содержать не менее 10 символов"` |
| `422` | Invalid JSON | Missing required field / wrong type |
| `500` | Internal server error | `"Internal server error"` |

---

## 📋 Data Models

### `ContactForm` — Input model

```python
class ContactForm(BaseModel):
    name: str         # Name
    phone: str        # Phone number
    email: EmailStr   # Email (with format validation)
    subject: str      # Subject
    message: str      # Message (min. 10 characters)
```

### `ContactResponse` — API response

```python
class ContactResponse(BaseModel):
    status: str       # Status ("success")
    message: str      # Result description
    telegram_sent: bool  # Whether delivered to Telegram
```

---

## ⚙️ Configuration

All variables are set via the `.env` file:

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `BOT_TOKEN` | `string` | ✅ | — | Telegram bot token (from [@BotFather](https://t.me/BotFather)) |
| `CHAT_ID` | `string` | ✅ | — | Chat/group ID for receiving messages |
| `CORS_ORIGINS` | `string[]` | ✅ | `["*"]` | Allowed CORS origins |
| `APP_HOST` | `string` | ✅ | `0.0.0.0` | Host to bind to |
| `APP_PORT` | `integer` | ✅ | `8000` | Server port |
| `APP_DEBUG` | `boolean` | ✅ | `false` | Debug mode |
| `TELEGRAM_PROXY_URL` | `string` | ❌ | `None` | Proxy for Telegram API |

### 🔒 Proxy

If Telegram API is blocked, configure a proxy:

```env
# SOCKS5
TELEGRAM_PROXY_URL=socks5://user:pass@host:port

# SOCKS4
TELEGRAM_PROXY_URL=socks4://user:pass@host:port

# HTTP(S)
TELEGRAM_PROXY_URL=http://user:pass@host:port
```

### 🌐 CORS

For frontend integration, specify its domain:

```env
CORS_ORIGINS=["https://dushafullstack.ru", "http://localhost:3000"]
```

To allow all origins (development only!):

```env
CORS_ORIGINS=["*"]
```

---

## 🐳 Docker

### Build and run

```bash
cd Docker
docker-compose up --build -d
```

### Stop

```bash
docker-compose down
```

### Healthcheck

The container automatically checks health every 30 seconds:

```bash
curl http://localhost:8080/health
```

---

## 🔧 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.12 |
| Web framework | FastAPI | 0.136.1 |
| Validation | Pydantic | 2.13.4 |
| Telegram | aiogram | 3.28.2 |
| Proxy | aiohttp-socks | 0.11.0 |
| ASGI server | Uvicorn | 0.46.0 |
| Prod server | Gunicorn | — |
| Containerization | Docker | — |

---

## 📜 License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">

**Made with ❤️ for [Dusha Fullstack](https://dushafullstack.ru)**

</div>
