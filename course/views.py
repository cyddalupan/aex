from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import CourseForm
from course.models import Course
from login.models import EmailUser

from shared.shared_functions import checkLogin

# Create your views here.
def list(request):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  user_id = request.COOKIES.get('user_id')
  user = EmailUser.objects.get(pk=user_id)
  courses = Course.objects.filter(user=user)
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
  return render(request, 'course/add.html', {'form': form})
def edit(request, course_id):
  if not checkLogin(request):
      return redirect(reverse('error-message'))
  instance = get_object_or_404(Course, pk=course_id)
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      instance.name = form.cleaned_data['name']
      instance.description = form.cleaned_data['description']
      instance.save()
      return redirect(reverse('course-list'))
  else:
    # Initialize the form with the instance data
    form = CourseForm(initial={
      'name': instance.name,
      'description': instance.description,
    })
  return render(request, 'course/add.html', {'form': form})