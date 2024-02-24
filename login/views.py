from venv import logger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
