import json

from django.core.management.base import BaseCommand

from apps.quiz.models import Answer, Category, Question, Subject


class Command(BaseCommand):
    help = 'Generate fake data for Subjects, Questions, and Answers'

    def handle(self, *args, **kwargs):
        # Создаем предмет
        subject, _ = Subject.objects.get_or_create(
            name="Matematika",
            language="uz"
        )
        Question.objects.filter(subject=subject).delete()
        self.stdout.write(self.style.SUCCESS(
            f'Subject "{subject.name}" created'))

        # Чтение данных из JSON файла
        with open('apps/quiz/datas/matematika.json', 'r', encoding='utf-8') as file:
            data_list = json.load(file)

        answers = []
        for item in data_list:
            ans_item = item.get('answers')
            correct_answer = item.get('correct_answer')
            category, _ = Category.objects.get_or_create(
                subject_id=subject.id,
                name=correct_answer.get('theme_id')
            )
            question = Question.objects.create(
                category=category,
                text=item.get('question'),
                code=item.get('question_number'),
                subject=subject,
                is_active=True
            )
            answers += [
                Answer(
                    question=question,
                    text=answer_text,
                    is_correct=(key == correct_answer.get('answer'))
                )
                for key, answer_text in ans_item.items()
            ]

            # Массово создаем ответы
        Answer.objects.bulk_create(answers)

        # self.stdout.write(self.style.SUCCESS(
        #     f'Question "{question.text}" with answers created'))

        self.stdout.write(self.style.SUCCESS(
            'All data successfully generated!'))
