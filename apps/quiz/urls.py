from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CheckAnswersView, QuestionViewSet, RandomQuestionListView,
                    SubjectListView, SubjectRecommendationListView)

router = DefaultRouter()
router.register('api/questions', QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/questions/random/',
         RandomQuestionListView.as_view(), name='random-question-list'),
    path('questions/<int:pk>/check-answers/',
         CheckAnswersView.as_view(), name='check-answers'),
    path('recommmendations/', SubjectRecommendationListView.as_view())
]
