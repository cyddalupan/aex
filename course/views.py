from django.shortcuts import redirect, render
from django.urls import reverse

from shared.shared_functions import checkLogin

# Create your views here.
def list(request):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  return render(request, 'course/list.html')