import json
import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.quiz.models import (Answer, Question,  # Замените на ваше приложение
                              Subject)


class Command(BaseCommand):
    help = 'Generate fake data for Subjects, Questions, and Answers'

    def handle(self, *args, **kwargs):

        subject, _ = Subject.objects.get_or_create(
            name="Ingliz tili",
            language="uz",
            question_count=20,
            question_time=500,
            image=None
        )
        self.stdout.write(self.style.SUCCESS(
            f'Subject "{subject.name}" created'))

        with open('apps/quiz/datas/english.json', 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        answers = []
        for item in data_list:
            # print(item)
            question = Question.objects.create(
                text=item.get('question'),
                code=item.get('question_number'),
                subject_id=subject.id
            )
            ans_item = item.get('answers')
            answers.append(Answer(
                question_id=question.id,
                text=ans_item.get('A'),
                is_correct=True
            ))
            answers.append(Answer(
                question_id=question.id,
                text=ans_item.get('B'),
                is_correct=False
            ))
            answers.append(Answer(
                question_id=question.id,
                text=ans_item.get('C'),
                is_correct=False
            ))
            answers.append(Answer(
                question_id=question.id,
                text=ans_item.get('D'),
                is_correct=False
            ))
        Answer.objects.bulk_create(answers)
