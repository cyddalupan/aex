from django.shortcuts import render

# Create your views here.
def terms(request):
  return render(request, 'content/terms.html')

def errorMessage(request):
  no_user = True
  return render(request, 'content/error_message.html', {'no_user': no_user})
