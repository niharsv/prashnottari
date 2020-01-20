from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from captcha.fields import CaptchaField
from django.forms.widgets import PasswordInput, TextInput
from .models import Question, Answer, Profile

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'write your answer'}),
        }

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'write your question'}),
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio',)
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'write your bio'}),
        }

class CustomAuthForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    captcha = CaptchaField();