from audioop import reverse
from django.shortcuts import redirect, render
from course.models import Course

from shared.shared_functions import checkLogin

# Create your views here.
def list(request, course_id):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  course = Course.objects.get(pk=course_id)
  return render(request, 'exam/list.html', {'course': course})

def add(request, course_id):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  error_messages = []
  if request.method == 'POST':     
      name = request.POST.get('name', '')
      email = request.POST.get('email', '')

      if not name:
          error_messages.append("Please enter your name.")
      # user_id = request.COOKIES.get('user_id')
      # user = EmailUser.objects.get(pk=user_id)
      # if form.is_valid():
      #     course  = Course(
      #         user = user,
      #         name = form.cleaned_data['name'],
      #         description = form.cleaned_data['description']
      #     )
      #     course.save()
      #     return redirect(reverse('course-list'))
  #else:
    # form = CourseForm()
  return render(request, 'exam/form.html', {'error_messages': error_messages})
