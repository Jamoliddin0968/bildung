import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.quiz.models import Subject, Question, Answer  # Замените на ваше приложение

class Command(BaseCommand):
    help = 'Generate fake data for Subjects, Questions, and Answers'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Генерация данных для предметов
        languages = ['ru', 'uz']
        for _ in range(10):  # Создадим 5 предметов
            subject = Subject.objects.create(
                name=faker.word(),
                language=random.choice(languages),
                question_count=20,  # количество вопросов
                question_time=random.randint(30, 120),  # время на вопрос в секундах
                image=None  # Если нужно добавить изображение, это можно сделать позже
            )
            self.stdout.write(self.style.SUCCESS(f'Subject "{subject.name}" created'))

            # Генерация вопросов для каждого предмета
            for _ in range(100):
                question = Question.objects.create(
                    text=faker.sentence(),
                    code=faker.random_number(digits=5, fix_len=True),
                    subject=subject
                )
                self.stdout.write(self.style.SUCCESS(f'  Question "{question.text}" created'))

                answer=None
                for _ in range(4):  # Создадим 4 ответа для каждого вопроса
                    answer = Answer.objects.create(
                        question=question,
                        text=faker.sentence(),
                        is_correct=False
                    )
                answer.is_correct=True
                answer.save()
                    