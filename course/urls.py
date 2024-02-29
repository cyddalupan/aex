from django.urls import path
from . import views
   
urlpatterns = [
    path('list', views.list, name='course-list'),
    path('add', views.add, name='course-add'),
    path('edit/<int:course_id>/', views.edit, name='course-edit'),
]