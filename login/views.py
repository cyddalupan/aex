import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib import messages
from shared_functions import SendEmail, checkLogin, generate_random_string
from .models import EmailUser

from .forms import EmailLoginForm, LoginCodeVerificationForm

# Create your views here.
def login(request):
  if request.method == 'POST':
    form = EmailLoginForm(request.POST)
    if form.is_valid():
      vcode = ''.join(random.choices('0123456789', k=6))
      if EmailUser.objects.filter(email=form.cleaned_data['email']).exists():
        user = EmailUser.objects.get(email=form.cleaned_data['email'])
        user.verify_code = vcode
      else:
        user = EmailUser(email=form.cleaned_data['email'], verify_code=vcode)
      user.save()
      url = reverse('send-verification-code', args=[user.id])
      request.session['allow_send_email'] = True
      return redirect(url)
  else:
    if checkLogin(request):
      return redirect(reverse('dashboard'))
    form = EmailLoginForm()
  return render(request, 'login/login.html', {'form': form})

def sendVerificationCode(request, user_id):
  if request.session.get('allow_send_email', False):
    try:
      user = EmailUser.objects.get(pk=user_id)
      verify_code = user.verify_code
      to = user.email
      subject = "Your AutoExam Verification Code"
      body =  f'''
      Thank you for choosing AutoExam!

      To ensure the security of your account, we require a six-digit verification code. Please use the following code to complete the verification process:

      Verification Code: [{verify_code}]

      Please enter this code within the app to confirm your identity and access your account.

      If you did not request this code or need any assistance, please don't hesitate to contact our support team at [autoexamapp@gmail.com]. We're here to help!

      Best regards,
      The AutoExam Team
      '''
      # TODO: Fix send email
      # SendEmail(to, subject, body)
      url = reverse('verify-login', args=[user_id])
      return redirect(url)
    except EmailUser.DoesNotExist:
      messages.error(request, "User does not exist.")
      return redirect(reverse('error-message'))

  else:
    return redirect(reverse(''))

def verifyLogin(request, user_id):
  user = EmailUser.objects.get(pk=user_id)
  if request.method == 'POST':
    form = LoginCodeVerificationForm(request.POST)
    if form.is_valid():
      if form.cleaned_data['verification_code'] == user.verify_code:
        login_token = generate_random_string(99)
        user.login_token = login_token
        user.save()
        response = HttpResponseRedirect(reverse('dashboard'))
        response.set_cookie('user_id', user_id)
        if form.cleaned_data['keep_logged_in']:
          response.set_cookie('login_token', login_token)
        else:
          expiration_time = datetime.now() + timedelta(hours=4)
          response.set_cookie('login_token', login_token, expires=expiration_time)
        return response
      else:
        form.add_error("verification_code", "Invalid verification code. Please try again.")
  else:
    form = LoginCodeVerificationForm()
  return render(request, 'login/login.html', {'form': form})

def logout(request):
  response = HttpResponseRedirect('/')
  response.delete_cookie('user_id')
  response.delete_cookie('login_token')
  return response

@csrf_exempt
def googleLogin(request):
  return render(request, 'login/google_login.html')
