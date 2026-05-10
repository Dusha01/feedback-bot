import logging
from fastapi import APIRouter, HTTPException, Depends

from src.models.schemas import ContactForm, ContactResponse
from src.services.telegram_service import TelegramService
from src.utils.validators import validate_contact_form



rt = APIRouter(prefix="/api", tags=["contact"])


@rt.post("/contact", response_model=ContactResponse)
async def contact_form(
    form: ContactForm,
    telegram_service: TelegramService = Depends()
):
    try:
        validate_contact_form(form)
        
        telegram_sent = await telegram_service.send_notification(form)
        
        if not telegram_sent:
            logging.warning("Telegram notification failed, but form data received")
        
        logging.info(f"Contact form received: {form.name}, {form.email}, {form.subject}")
        
        return ContactResponse(
            status="success",
            message="Form submitted successfully",
            telegram_sent=telegram_sent
        )
        
    except ValueError as e:
        logging.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")