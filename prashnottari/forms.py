from django import forms

from .models import Question, Answer, Profile

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('text',)

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio',)        
