import json

from django.core.management.base import BaseCommand

from apps.quiz.models import Answer, Question, Subject


class Command(BaseCommand):
    help = 'Generate fake data for Subjects, Questions, and Answers'

    def handle(self, *args, **kwargs):
        # Создаем предмет
        subject, _ = Subject.objects.get_or_create(
            name="Biologiya",
            language="uz",
            question_count=20,
            question_time=500,
            image=None
        )
        self.stdout.write(self.style.SUCCESS(
            f'Subject "{subject.name}" created'))

        # Чтение данных из JSON файла
        with open('apps/quiz/datas/biology.json', 'r', encoding='utf-8') as file:
            data_list = json.load(file)

        # Обработка вопросов и ответов
        for item in data_list:
            # Создаем вопрос
            question = Question.objects.create(
                text=item.get('question'),
                code=item.get('question_number'),
                subject=subject  # Указываем объект subject напрямую
            )

            # Получаем ответы и создаем объекты Answer
            ans_item = item.get('answers')
            # получаем правильный ответ
            correct_answer = item.get('correct_answer')

            # Создаем список объектов Answer для bulk_create
            answers = [
                Answer(
                    question=question,
                    text=answer_text,
                    # помечаем правильный ответ
                    is_correct=(key == correct_answer)
                )
                for key, answer_text in ans_item.items()
            ]

            # Массово создаем ответы
            Answer.objects.bulk_create(answers)

            self.stdout.write(self.style.SUCCESS(
                f'Question "{question.text}" with answers created'))

        self.stdout.write(self.style.SUCCESS(
            'All data successfully generated!'))
