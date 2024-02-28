import smtplib
import string
import secrets
from django.urls import reverse
from django.shortcuts import redirect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from login.models import EmailUser
from django.contrib import messages

def SendEmail(to, subject, body):
  # Email configuration
  email_sender = 'autoexamapp@gmail.com'
  email_receiver = to
  email_subject = subject
  email_body = body

  # Create a MIMEText object to represent the email content
  msg = MIMEMultipart()
  msg['From'] = email_sender
  msg['To'] = email_receiver
  msg['Subject'] = email_subject

  # Attach the email body
  msg.attach(MIMEText(email_body, 'plain'))

  # Connect to the SMTP server (e.g., Gmail's SMTP server)
  smtp_server = 'smtp.gmail.com'
  smtp_port = 587
  smtp_username = 'autoexamapp@gmail.com'
  smtp_password = 'tqzd atpd ewum qcct'

  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Start TLS encryption
    server.login(smtp_username, smtp_password)
    server.sendmail(email_sender, email_receiver, msg.as_string())

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def checkLogin(request):
  user_id = request.COOKIES.get('user_id')
  login_token = request.COOKIES.get('login_token')

  try:
    user = EmailUser.objects.get(pk=user_id)
    if user.login_token != login_token:
      messages.error(request, "Login expired please login again.")
      return False
    else:
      return True
  except EmailUser.DoesNotExist:
    messages.error(request, "Login expired please login again.")
    return False