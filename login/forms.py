from django import forms
from captcha.fields import CaptchaField

from shared.bootstrap_form import BootstrapForm

class EmailLoginForm(BootstrapForm):
    email = forms.EmailField(label='Your Email')
    captcha = CaptchaField()

class LoginCodeVerificationForm(BootstrapForm):
    verification_code = forms.CharField(label='Verification Code', max_length=6, min_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code'}))
    keep_logged_in = forms.BooleanField(label='Keep me logged in', required=False)