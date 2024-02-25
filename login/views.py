from venv import logger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from captcha.fields import CaptchaField

from .forms import ContactForm

# Create your views here.
def login(request):
  if request.method == 'POST':
      form = ContactForm(request.POST)
      if form.is_valid():
        print("Form data: %s", form.cleaned_data)
  else:
      form = ContactForm()
  return render(request, 'login/login.html', {'form': form})

@csrf_exempt
def googleLogin(request):
  return render(request, 'login/google_login.html')

def sendEmail(request):
  # Email configuration
  email_sender = 'autoexamapp@gmail.com'
  email_receiver = 'cydmdalupan@gmail.com'
  email_subject = 'Subject: First Test Email'
  email_body = 'Your email body goes here.'

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

  print('Email sent successfully.')