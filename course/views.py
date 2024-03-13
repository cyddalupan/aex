from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import CourseForm
from course.models import Course
from login.models import EmailUser
from django.contrib import messages

from shared.shared_functions import checkLogin

# Create your views here.
def list(request):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  user_id = request.COOKIES.get('user_id')
  user = EmailUser.objects.get(pk=user_id)
  courses = Course.objects.filter(user=user, deleted_at__isnull=True)
  return render(request, 'course/list.html', {'courses': courses})

def add(request):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  if request.method == 'POST':
      form = CourseForm(request.POST)
      user_id = request.COOKIES.get('user_id')
      user = EmailUser.objects.get(pk=user_id)
      if form.is_valid():
          course  = Course(
              user = user,
              name = form.cleaned_data['name'],
              description = form.cleaned_data['description']
          )
          course.save()
          return redirect(reverse('course-list'))
  else:
    form = CourseForm()
  return render(request, 'course/form.html', {'form': form})

def edit(request, course_id):
    if not checkLogin(request):
        return redirect(reverse('error-message'))
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.description = form.cleaned_data['description']
            course.save()
            return redirect(reverse('course-list'))
    else:
        # Initialize the form with the instance data
        form = CourseForm(initial={
            'name': course.name,
            'description': course.description,
        })

    return render(request, 'course/form.html', {
       'form': form,
       'is_edit': True
    })

def delete(request, course_id):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  course = get_object_or_404(Course, pk=course_id)
  user_id = request.COOKIES.get('user_id')
  user = EmailUser.objects.get(pk=user_id)
  if user != course.user:
      messages.error(request, "Login expired please login again.")
      return redirect(reverse('error-message'))
  course.delete()
  return redirect(reverse('course-list'))