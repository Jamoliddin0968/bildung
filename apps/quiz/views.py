import random

from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core.paginations import CustomPagination

from .models import Answer, Question, Subject
from .serializers import (AnswerSerializer, QuestionCreateSerializer,
                          QuestionSerializer, SubjectSerializer)


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
    queryset = Question.objects.all()

    def get(self, request, pk, format=None):
        subject = get_object_or_404(Subject, pk=pk)
        question_count = subject.question_count
        answers_queryset = Answer.objects.order_by('?')
        questions = Question.objects.filter(
            subject=subject, is_active=True).prefetch_related(
            Prefetch('answers', queryset=answers_queryset)
        ).order_by('?')[:question_count]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class CheckAnswersView(APIView):
    def post(self, request, pk, format=None):
        question = get_object_or_404(Question, pk=pk)
        given_answers = request.data.get('answers', [])

        correct_answers = question.answers.filter(is_correct=True)
        correct_answers_ids = [answer.id for answer in correct_answers]

        is_correct = set(given_answers) == set(correct_answers_ids)

        return Response({
            'is_correct': is_correct,
            'correct_answers': AnswerSerializer(correct_answers, many=True).data
        }, status=status.HTTP_200_OK)


class SubjectRecommendationListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        language = self.request.query_params.get('language') or 'uz'
        language = language.lower()
        if language:
            return self.queryset.filter(language=language)
        return self.queryset.order_by("?")


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
