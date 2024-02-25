from django.urls import path
from . import views
   
urlpatterns = [
    path('', views.login, name='login'),
    path('google-login', views.googleLogin, name='login_google'),
    path('send-email', views.sendEmail, name='send-email'),
]
