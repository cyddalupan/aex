import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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