from django import forms

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Loop through all fields and update their widget attributes
        for field_name, field in self.fields.items():
            # Check if the field already has the 'class' attribute set
            existing_classes = field.widget.attrs.get('class', '')
            
            # Add 'form-control' class to the existing classes
            field.widget.attrs['class'] = f'{existing_classes} form-control'
            
            # Add support for buttons and dropdowns
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = f'{existing_classes} custom-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = f'{existing_classes} custom-control-input'
            elif isinstance(field.widget, (forms.DateInput, forms.DateTimeInput, forms.TimeInput)):
                field.widget.attrs['class'] = f'{existing_classes} form-control datetimepicker-input'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = f'{existing_classes} custom-file-input'
