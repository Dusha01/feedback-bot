from aiogram import Bot
from aiogram.enums import ParseMode
import logging

from src.config import settings
from src.telegram_session import create_telegram_aiohttp_session



class TelegramService:
    def __init__(self):
        self.bot = None
        self.chat_id = settings.CHAT_ID
        
        if settings.BOT_TOKEN:
            session = create_telegram_aiohttp_session(settings.TELEGRAM_PROXY_URL)
            self.bot = Bot(token=settings.BOT_TOKEN, session=session)
    
    async def send_notification(self, form_data) -> bool:
        if not self.bot or not self.chat_id:
            logging.warning("Telegram bot not configured")
            return False
        
        try:
            message_text = f"""
📧 *Новое сообщение с сайта*

*Имя:* {form_data.name}
*Телефон:* {form_data.phone}
*Email:* {form_data.email}
*Тема:* {form_data.subject}

*Сообщение:*
{form_data.message}
            """
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN
            )
            return True
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False

telegram_service = TelegramService()