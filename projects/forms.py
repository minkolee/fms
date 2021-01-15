from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name', 'address', 'manager', 'active', 'text',)
        widgets = {
            'name': forms.TextInput(),
            'address': forms.TextInput(),
            'manager': forms.TextInput(),
            'text': forms.Textarea(),
        }
