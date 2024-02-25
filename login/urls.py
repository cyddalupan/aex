from django.urls import path
from . import views
   
urlpatterns = [
    path('', views.login, name='login'),
    path('send-verification-code/<int:user_id>/', views.sendVerificationCode, name='send-verification-code'),
    path('verify-login', views.verifyLogin, name='verify-login'),

    ## Inactive
    path('google-login', views.googleLogin, name='login_google'),
]
