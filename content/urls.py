from django.urls import path
from . import views
   
urlpatterns = [
    path('terms/', views.terms, name='terms'),
    path('error-message/', views.errorMessage, name='error-message'),
]
