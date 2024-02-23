from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login(request):
  return render(request, 'login/login.html')

@csrf_exempt
def googleLogin(request):
  return render(request, 'login/google_login.html')
