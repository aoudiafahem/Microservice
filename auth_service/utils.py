import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
import models
import datetime
import os
from otp_html import otp_html 

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str, name: str = ""):
    try:
        service_email = os.getenv("service_email")
        service_password = os.getenv("service_password")

        msg = MIMEText(otp_html(otp, name), "html")  
        msg["Subject"] = "🔒 Your OTP Code"
        msg["From"] = service_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(service_email, service_password)
            server.send_message(msg)

        print(f"✅ OTP email sent successfully to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send OTP email to {to_email}: {e}")








def store_otp(db: Session, user_id: int, otp: str):
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    db_otp = models.OTP(user_id=user_id, otp=otp, expiration_time=expiration_time)
    db.add(db_otp)
    db.commit()

def verify_otp(db: Session, email: str, otp: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False, "User not found"

    otp_record = (
        db.query(models.OTP)
        .filter(models.OTP.user_id == user.id)
        .order_by(models.OTP.id.desc())
        .first()
    )

    if not otp_record or otp_record.expiration_time < datetime.datetime.now():
        return False, "OTP invalid or expired"

    if otp_record.otp != otp:
        return False, "OTP incorrect"

    return True, user
