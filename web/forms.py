from django import forms
from .models import Application, ContactMessage


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'child_name', 'date_of_birth', 'gender', 'class_applying_for',
            'previous_school', 'parent_name', 'phone', 'email',
            'address', 'message',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 4})}