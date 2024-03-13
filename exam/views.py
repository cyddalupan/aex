import uuid
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Count
from course.models import Course
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from .models import Exam

from shared.shared_functions import checkLogin

load_dotenv()
client = OpenAI()

# Create your views here.
def list(request, course_id):
    if not checkLogin(request):
        return redirect(reverse('error-message'))
    course = Course.objects.get(pk=course_id)
    exams = Exam.objects.filter(course=course, deleted_at__isnull=True)
    return render(request, 'exam/list.html', {
        'course': course,
        'exams': exams
    })

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
            order = Exam.objects.filter(course=course).aggregate(count=Count('id'))['count'] or 0
            if not exam["is_video"]:
                audio_url = "audio/" + str(uuid.uuid4()) + ".mp3"
                speech_file_path = Path(__file__).parent.parent / audio_url
                response = client.audio.speech.create(
                    model="tts-1",
                    voice="shimmer",
                    input=exam["lesson"]
                )
                response.stream_to_file(speech_file_path)

            examModel = Exam(
                course = course,
                title = exam["title"],
                lesson = exam["lesson"],
                audio_url = audio_url,
                video_embed = exam["youtube"],
                answer = exam["answer"],
                is_video = exam["is_video"],
                order = order,
            )
            examModel.save()
            url = reverse('exam-list', args=[course_id])
            return redirect(url)

    return render(request, 'exam/form.html', {
        'course_id': course_id,
        'exam': exam,
        'error_messages': error_messages,
    })

def edit(request, exam_id):
    if not checkLogin(request):
        return redirect(reverse('error-message'))
    error_messages = []

    exam = Exam.objects.get(pk=exam_id)
    course_id = exam.course.id

    exam = {
        "title" : exam.title,
        "is_video" : exam.is_video,
        "audio_url" : exam.audio_url,
        "lesson" : exam.lesson,
        "youtube" : exam.video_embed,
        "answer" : exam.answer
    }

    return render(request, 'exam/form.html', {
        'is_edit': True,
        'course_id': course_id,
        'exam': exam,
        'error_messages': error_messages,
    })