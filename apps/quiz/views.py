from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Subject, Question, Answer
from .serializers import SubjectSerializer, QuestionSerializer, AnswerSerializer
from django.db.models import Count
import random

# 1. Список предметов с пагинацией и фильтрацией по языку
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = None  # Можно подключить стандартный пагинатор или кастомный

    def get_queryset(self):
        language = self.request.query_params.get('language')
        if language:
            return self.queryset.filter(language=language)
        return self.queryset


# 2. Случайный список вопросов
class RandomQuestionListView(APIView):

    def get(self, request, pk, format=None):
        subject = get_object_or_404(Subject, pk=pk)
        question_count = subject.question_count
        questions = list(subject.questions.all())
        random.shuffle(questions)
        selected_questions = questions[:question_count]
        serializer = QuestionSerializer(selected_questions, many=True)
        return Response(serializer.data)


# 3. Проверка ответов и возврат правильных ответов
class CheckAnswersView(APIView):

    def post(self, request, pk, format=None):
        question = get_object_or_404(Question, pk=pk)
        given_answers = request.data.get('answers', [])  # Ожидаемый формат: {"answers": [1, 2, 3]}
        
        # Получаем правильные ответы
        correct_answers = question.answers.filter(is_correct=True)
        correct_answers_ids = [answer.id for answer in correct_answers]

        # Проверяем, совпадают ли переданные ответы с правильными
        is_correct = set(given_answers) == set(correct_answers_ids)

        # Формируем ответ
        return Response({
            'is_correct': is_correct,
            'correct_answers': AnswerSerializer(correct_answers, many=True).data
        }, status=status.HTTP_200_OK)
