from django import forms
from django.core.exceptions import ValidationError

from shared.bootstrap_form import BootstrapForm

class CourseForm(BootstrapForm):
    name = forms.CharField(label='Name', max_length=100, required=True)
    description = forms.CharField(label='Description', max_length=255, required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Check if name is provided
        if not name:
            raise ValidationError("Name is required.")

        return name