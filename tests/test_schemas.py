import pytest
from pydantic import ValidationError

from src.models.schemas import ContactForm, ContactResponse


class TestContactForm:
    def test_valid_form(self, valid_form_data):
        form = ContactForm(**valid_form_data)
        assert form.name == "Иван Иванов"
        assert form.phone == "+7 (999) 123-45-67"
        assert form.email == "ivan@example.com"
        assert form.subject == "Сотрудничество"
        assert form.message == "Здравствуйте! Хотел бы обсудить сотрудничество."

    def test_missing_name_raises(self, valid_form_data):
        del valid_form_data["name"]
        with pytest.raises(ValidationError):
            ContactForm(**valid_form_data)

    def test_missing_email_raises(self, valid_form_data):
        del valid_form_data["email"]
        with pytest.raises(ValidationError):
            ContactForm(**valid_form_data)

    def test_invalid_email_raises(self, valid_form_data):
        valid_form_data["email"] = "not-an-email"
        with pytest.raises(ValidationError):
            ContactForm(**valid_form_data)

    def test_missing_message_raises(self, valid_form_data):
        del valid_form_data["message"]
        with pytest.raises(ValidationError):
            ContactForm(**valid_form_data)

    def test_empty_string_fields(self, valid_form_data):
        valid_form_data["name"] = ""
        valid_form_data["subject"] = ""
        form = ContactForm(**valid_form_data)
        assert form.name == ""
        assert form.subject == ""


class TestContactResponse:
    def test_default_values(self):
        resp = ContactResponse(status="success", message="ok")
        assert resp.telegram_sent is False

    def test_custom_values(self):
        resp = ContactResponse(status="success", message="ok", telegram_sent=True)
        assert resp.telegram_sent is True
