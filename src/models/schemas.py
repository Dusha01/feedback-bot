from pydantic import BaseModel, EmailStr

class ContactForm(BaseModel):
    name: str
    phone: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(BaseModel):
    status: str
    message: str
    telegram_sent: bool = False