import random
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from shared_functions import SendEmail
from .models import EmailUser

from .forms import EmailLoginForm, LoginCodeVerificationForm

# Create your views here.
def login(request):
  if request.method == 'POST':
    form = EmailLoginForm(request.POST)
    if form.is_valid():
      print("Form data: %s", form.cleaned_data)
      print("Email data: %s", form.email)
      vcode = ''.join(random.choices('0123456789', k=6))
      if EmailUser.objects.filter(email=form.email).exists():
        user = EmailUser.objects.get(email=form.email)
        user.verify_code = vcode
      else:
        user = EmailUser(email=form.email, verify_code=vcode)
      user.save()
      url = reverse('send-verification-code', args=[user.id])
      request.session['allow_send_email'] = True
      return redirect(url)
  else:
    # TODO: Check cookie or session
      # TODO: Login user and redirect
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
      SendEmail(to, subject, body)
      return redirect('verify-login')
    except EmailUser.DoesNotExist:
      messages.error(request, "User does not exist.")
      return redirect('content/error-message/')
  else:
    return redirect(reverse(''))

def verifyLogin(request):
  if request.method == 'POST':
    ## TODO: compare code if true
      ## TODO: Check if keep me logged is check then store cookie if active
        ## TODO: Redirect and save long term cookie
      ## TODO: not stay logged
        ## TODO: Redirect save and Cookie with expiration
    ## TODO: failed return error
  
  ## TODO: enter verify page
  ## TODO: Keep me logged in
  ## TODO: confirm 
  form = LoginCodeVerificationForm()
  return render(request, 'login/login.html', {'form': form})

## TODO: Logout
  ## TODO: DELETE COOKIE

@csrf_exempt
def googleLogin(request):
  return render(request, 'login/google_login.html')
