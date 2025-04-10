import random
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    sender_email = "pradeepcollegeproject123@gmail.com"
    sender_password = "pradeep@123"
    subject = "Your OTP Verification Code"
    message = f"Dear User,\n\nYour OTP for registration at AITS Tirupati, is: {otp}\n\nThis OTP is valid for [5 or 10] minutes. Please do not share it with anyone.\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nYour developer Pradeep from AITS Titupati"


    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
