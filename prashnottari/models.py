from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=255)
    asker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.TextField(max_length=5000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:20]

class Profile(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.name
