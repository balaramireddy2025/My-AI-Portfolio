from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, ValidationError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

conf = ConnectionConfig(
    MAIL_USERNAME="ybalaramireddy@gmail.com",
    MAIL_PASSWORD="Yarram@123",
    MAIL_FROM="ybalaramireddy@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,       # <-- use MAIL_STARTTLS instead of MAIL_TLS
    MAIL_SSL_TLS=False,       # <-- use MAIL_SSL_TLS instead of MAIL_SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@router.get("/contact")
def contact_form(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/contact")
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    try:
        EmailStr.validate(email)
    except ValidationError:
        return templates.TemplateResponse("contact.html", {"request": request, "error": "Invalid email"})
    
    msg = MessageSchema(
        subject=f"Portfolio Contact: {name}",
        recipients=["your_email@gmail.com"],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(msg)
    return templates.TemplateResponse("contact.html", {"request": request, "success": "Message sent successfully!"})
