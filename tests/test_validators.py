import pytest

from src.utils.validators import validate_contact_form


class TestValidateContactForm:
    def test_valid_form(self, valid_form):
        validate_contact_form(valid_form)

    def test_empty_name_raises(self, valid_form):
        valid_form.name = ""
        with pytest.raises(ValueError, match="Имя обязательно"):
            validate_contact_form(valid_form)

    def test_whitespace_name_raises(self, valid_form):
        valid_form.name = "   "
        with pytest.raises(ValueError, match="Имя обязательно"):
            validate_contact_form(valid_form)

    def test_empty_message_raises(self, valid_form):
        valid_form.message = ""
        with pytest.raises(ValueError, match="Сообщение обязательно"):
            validate_contact_form(valid_form)

    def test_whitespace_message_raises(self, valid_form):
        valid_form.message = "   "
        with pytest.raises(ValueError, match="Сообщение обязательно"):
            validate_contact_form(valid_form)

    def test_short_message_raises(self, valid_form):
        valid_form.message = "Короткое"
        with pytest.raises(ValueError, match="не менее 10 символов"):
            validate_contact_form(valid_form)

    def test_exactly_10_chars_message_ok(self, valid_form):
        valid_form.message = "1234567890"
        validate_contact_form(valid_form)

    def test_long_message_ok(self, valid_form):
        valid_form.message = "A" * 1000
        validate_contact_form(valid_form)
