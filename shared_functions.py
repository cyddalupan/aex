import smtplib
import string
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.shortcuts import redirect
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

def errorMessage(request, Message):
  messages.error(request, Message)
  return redirect('content/error-message/')

def checkLogin(request):
  # Get user_id From Cookies
  if 'user_id' not in request.COOKIES:
    return errorMessage(request, "user_id does not exist.")
  user_id = request.COOKIES.get('user_id')
  
  # Get login_token From Cookies
  if 'login_token' not in request.COOKIES:
    return errorMessage(request, "login_token does not exist.")
  login_token = request.COOKIES.get('login_token')

  # Check if token match
  try:
    user = EmailUser.objects.get(pk=user_id)
    if user.login_token != login_token:
      return redirect("")
  except EmailUser.DoesNotExist:
    return errorMessage(request, "User does not exist.")