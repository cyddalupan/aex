from django.urls import path
from . import views
   
urlpatterns = [
    path('', views.login, name='login'),
    path('send-verification-code/<int:user_id>/', views.sendVerificationCode, name='send-verification-code'),
    path('verify-login/<int:user_id>/', views.verifyLogin, name='verify-login'),
    path('logout', views.logout, name='logout'),

    ## Inactive
    path('google-login', views.googleLogin, name='login_google'),
]
