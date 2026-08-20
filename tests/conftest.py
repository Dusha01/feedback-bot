import sys
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.models.schemas import ContactForm

_FAKE_TOKEN = "1234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"


@pytest.fixture(autouse=True)
def _mock_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", _FAKE_TOKEN)
    monkeypatch.setenv("CHAT_ID", "123")
    monkeypatch.setenv("CORS_ORIGINS", '["*"]')
    monkeypatch.setenv("APP_HOST", "0.0.0.0")
    monkeypatch.setenv("APP_PORT", "8000")
    monkeypatch.setenv("APP_DEBUG", "false")


@pytest.fixture
def client(_mock_env):
    # Clear cached src.* modules so config re-reads env vars
    for mod in list(sys.modules):
        if mod.startswith("src."):
            del sys.modules[mod]

    with patch("aiogram.Bot") as mock_bot_cls:
        mock_bot = mock_bot_cls.return_value
        mock_bot.send_message = AsyncMock(return_value=True)

        from src.main import app

        app.dependency_overrides = {}
        yield TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def valid_form_data() -> dict:
    return {
        "name": "Иван Иванов",
        "phone": "+7 (999) 123-45-67",
        "email": "ivan@example.com",
        "subject": "Сотрудничество",
        "message": "Здравствуйте! Хотел бы обсудить сотрудничество.",
    }


@pytest.fixture
def valid_form(valid_form_data) -> ContactForm:
    return ContactForm(**valid_form_data)
