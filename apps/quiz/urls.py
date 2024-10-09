from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BachelorProgramViewSet, CheckAnswersView,
                    CustomQuestionViewSet, CustomSubjectViewSet,
                    QuestionViewSet, RandomQuestionListView, SubjectListView,
                    SubjectRecommendationListView)

router = DefaultRouter()
router.register(r'subjects', CustomSubjectViewSet)
router.register(r'questions', CustomQuestionViewSet)
router.register(r'bachelorprograms', BachelorProgramViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/questions/random/',
         RandomQuestionListView.as_view(), name='random-question-list'),
    path('questions/<int:pk>/check-answers/',
         CheckAnswersView.as_view(), name='check-answers'),
    path('recommmendations/', SubjectRecommendationListView.as_view())
]
