from django.urls import path
from .views import HelloWorld

urlpatterns = [
    path('hello-world/', HelloWorld.as_view()),
]