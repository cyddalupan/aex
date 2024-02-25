from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)
    captcha = CaptchaField()