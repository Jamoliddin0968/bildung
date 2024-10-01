from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.core.paginations import CustomPagination
from .models import Subject, Question, Answer
from .serializers import SubjectSerializer, QuestionSerializer, AnswerSerializer
from django.db.models import Count
import random
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = CustomPagination  

    def get_queryset(self):
        language = self.request.query_params.get('language') or 'uz'
        language = language.lower()
        if language:
            return self.queryset.filter(language=language)
        return self.queryset


class RandomQuestionListView(GenericAPIView):
    serializer_class = QuestionSerializer

    def get(self, request, pk, format=None):
        subject = get_object_or_404(Subject, pk=pk)
        question_count = subject.question_count
        questions = Question.objects.filter(subject=subject).order_by('?')[:question_count]
        serializer = QuestionSerializer(questions, many=True)
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
            'is_correct': "sdbjh"
        }, status=status.HTTP_200_OK)
