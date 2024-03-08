from django.shortcuts import redirect, render
from django.urls import reverse
from course.models import Course
from .models import Exam

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

    exam = {
        "title" : "",
        "is_video" : False,
        "lesson" : "",
        "youtube" : "",
        "answer" : ""
    }
    if request.method == 'POST':  
        exam["title"] = request.POST.get('title', '')
        exam["is_video"] = request.POST.get('is_video', '')
        exam["lesson"] = request.POST.get('lesson', '')
        exam["youtube"] = request.POST.get('youtube', '')
        exam["answer"] = request.POST.get('answer', '')

        if not exam["title"]:
            error_messages.append("Title is required.")
        if len(exam["title"]) > 240:
            error_messages.append('Title exceeds maximum length of 240 characters.')
        if exam["is_video"]:
            exam["is_video"] = True
            if not exam["youtube"]:
                error_messages.append("Please embed a valid youtube video")
            if len(exam["youtube"]) > 800:
                error_messages.append('YouTube embed code exceeds maximum length of 800 characters.')
            if not exam["youtube"].startswith('<iframe') or not exam["youtube"].endswith('</iframe>'):
                error_messages.append('Invalid YouTube embed code. It must start with "<iframe" and end with "</iframe>".')
            if 'src="https://www.youtube.com/embed/' not in exam["youtube"]:
                error_messages.append('Invalid YouTube embed code. It must contain a valid YouTube video URL.')
        else:
            exam["is_video"] = False
            if not exam["lesson"]:
                error_messages.append("Please write a lesson")
            if len(exam["lesson"]) > 800:
                error_messages.append('Lesson exceeds maximum length of 800 characters.')
        if not exam["answer"]:
            error_messages.append("Please write your expected answer")
        if len(exam["answer"]) > 800:
            error_messages.append('Answer exceeds maximum length of 800 characters.')
        if len(error_messages) == 0:
            course = Course.objects.get(pk=course_id)
            examModel = Exam(
                course = course,
                title = exam["title"],
                audio_url = "",
                video_embed = exam["youtube"],
                answer = exam["answer"],
                is_video = exam["is_video"],
                order = 0,
            )
            examModel.save()
            url = reverse('exam-list', args=[course_id])
            return redirect(url)
    return render(request, 'exam/form.html', {
        'exam': exam,
        'error_messages': error_messages,
    })
