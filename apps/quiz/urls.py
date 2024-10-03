from django.urls import path

from .views import (CheckAnswersView, RandomQuestionListView, SubjectListView,
                    SubjectRecommendationListView)

urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/questions/random/',
         RandomQuestionListView.as_view(), name='random-question-list'),
    path('questions/<int:pk>/check-answers/',
         CheckAnswersView.as_view(), name='check-answers'),
    path('recommmendations/', SubjectRecommendationListView.as_view())
]
