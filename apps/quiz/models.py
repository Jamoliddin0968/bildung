from django.db import models
from django.db import models

class Subject(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('uz', 'Узбекский'),
    ]
    
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru')  # Поле выбора языка

    def __str__(self):
        return f"{self.name} ({self.get_language_display()})"


class Question(models.Model):
    text = models.CharField(max_length=255)
    code = models.CharField(max_length=20, blank=True, null=True) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"
