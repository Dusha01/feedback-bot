def validate_contact_form(form_data) -> None:
    if not form_data.name.strip():
        raise ValueError("Имя обязательно для заполнения")
    if not form_data.message.strip():
        raise ValueError("Сообщение обязательно для заполнения")
    if len(form_data.message) < 10:
        raise ValueError("Сообщение должно содержать не менее 10 символов")