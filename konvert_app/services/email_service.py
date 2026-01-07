# konvert_app/services/email_service.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://127.0.0.1:8000")
SMTP_FROM = os.getenv("SMTP_FROM", "Konvert <konvert-app@gmail.com>")

def send_verification_email(to_email: str, token: str):
    verify_url = f"{FRONTEND_BASE_URL}/verify-email?token={token}"

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = "Verify your email — Konvert"

    body = f"""
Hi 👋,

Welcome to Konvert!

Please verify your email address by clicking the link below:

{verify_url}

After verification, you can log in and start converting files.

If you did not create this account, you can safely ignore this email.

—
Konvert Team
"""

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))) as server:
        server.starttls()
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD"),
        )
        server.send_message(msg)
