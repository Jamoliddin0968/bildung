
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subject(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('uz', 'Узбекский'),
    ]

    name = models.CharField(max_length=100)
    language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, default='ru')  # Поле выбора языка
    # Поле для загрузки изображений
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    question_count = models.IntegerField(
        default=0)  # Поле для количества вопросов
    # Поле для времени на вопрос (в секундах)
    question_time = models.IntegerField(default=60)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_language_display()})"


class BachelorProgram(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

    first_subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True)
    # баллы для первого предмета с дефолтом 0
    first_subject_point = models.FloatField(default=0.0)

    second_subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="second_bachelor", null=True, blank=True)
    # баллы для второго предмета с дефолтом 0
    second_subject_point = models.FloatField(default=0.0)

    required_subject1 = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="required_subject_first", null=True, blank=True)
    required_subject1_point = models.FloatField(default=0.0)

    required_subject2 = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="required_subject_second", null=True, blank=True)
    required_subject2_point = models.FloatField(default=0.0)
    required_subject3 = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="required_subject_third", null=True, blank=True)
    required_subject3_point = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Category(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='themes', null=True, blank=True)
    name = models.CharField(max_length=127)


class Question(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    code = models.CharField(max_length=20, blank=True, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='questions')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class AudioFile(models.Model):
    file = models.FileField()
