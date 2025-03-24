
from django import forms
from .models import Collaborative, Application

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaborative
        fields = ['event_name', 'organizer', 'collaboration_descr', 'skills_preferred', 'team_size', 'deadline', 'contact_email']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    resume = forms.FileField(required=True)

    class Meta:
        model = Application
        fields = ['message', 'resume']
