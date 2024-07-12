from django import forms
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'code', 'content', 'topic']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }
       
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ['topic', 'language']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }


class TutorialTopicForm(forms.ModelForm):
    class Meta:
        model = TutorialPost
        # Exclude the user field from the form
        exclude = ['user']
        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'form-control'}),
            'post_file': forms.Textarea(attrs={'class': 'form-control'}),
            'post_video': forms.URLInput(attrs={'class': 'form-control'}),
            'post_content': forms.Textarea(attrs={'class': 'form-control'}),
            'tutorialName': forms.Select(attrs={'class': 'form-control'}),
        }


class TutorialForm(forms.ModelForm):
    class Meta:
        model = TutorialName
        fields = "__all__"
        widgets = {
            'tutorialName': forms.TextInput(attrs={'class': 'form-control'}),
            'tutorialContent': forms.Textarea(attrs={'class': 'form-control'}),
            'tutorialImage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdminPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.TextInput(attrs={'class':'form-control'})
        }