from django.urls import path
from . import views
   
urlpatterns = [
    path('list/<int:course_id>/', views.list, name='exam-list'),
    path('exam-add/<int:course_id>/', views.add, name='exam-add'),
    path('exam-edit/<int:exam_id>/', views.edit, name='exam-edit'),
]