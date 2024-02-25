from django.shortcuts import render

# Create your views here.
def terms(request):
  return render(request, 'content/terms.html')

def errorMessage(request):
  return render(request, 'content/error_message.html')
