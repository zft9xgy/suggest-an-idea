from django import forms
from .models import Idea, App

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description','app']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Idea title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'App name'}),
            'description': forms.Textarea(attrs={'placeholder': 'App Description'}),
        }