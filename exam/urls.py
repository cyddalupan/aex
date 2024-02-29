from django.urls import path
from . import views
   
urlpatterns = [
    path('list/<int:course_id>/', views.list, name='exam-list'),
]