import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from functools import lru_cache
import aiosmtplib
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

async def get_smtp_connection():
    smtp = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True, timeout=10)
    await smtp.connect()
    print(os.getenv("EMAIL_HOST_USER", ""), os.getenv("EMAIL_HOST_PASSWORD", ""))
    try:
        await smtp.login(os.getenv("EMAIL_HOST_USER", ""), os.getenv("EMAIL_HOST_PASSWORD", ""))
    except Exception as e:
        print(f"error: {e}")
    return smtp


@lru_cache(maxsize=100)
def render_personalized_text(username, verification_code):
    return f"""
    Dear {username},
    Thank you for joining our service. We are thrilled to have you on board! 🎉🎉
    Your account verification code is: {verification_code}
    Your verification code will expire in 15 minutes!!!
    Best regards,
    Miky Rola
    """

async def send_email(subject, verification_code, recipient_email, username="Friend"):
    sender_email = os.getenv("EMAIL_HOST_USER", default="")
    sender_name = "Research Project"
    formatted_sender = formataddr((sender_name, sender_email))
    formatted_recipient = formataddr((username, recipient_email))

    message = MIMEMultipart("alternative")
    message["From"] = formatted_sender
    message["To"] = formatted_recipient
    message["Subject"] = subject

    text_content = render_personalized_text(username, verification_code)
    message.attach(MIMEText(text_content, "plain"))

    smtp = await get_smtp_connection()

    try:
        await smtp.send_message(message)
        logger.info(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        raise  
    finally:
        await smtp.quit()