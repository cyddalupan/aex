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