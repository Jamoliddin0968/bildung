from django.urls import path
from .views import SubjectListView, RandomQuestionListView, CheckAnswersView

urlpatterns = [
    # 1. Получить список предметов с фильтрацией по языку
    path('subjects/', SubjectListView.as_view(), name='subject-list'),

    # 2. Получить случайный список вопросов для конкретного предмета
    path('subjects/<int:pk>/questions/random/', RandomQuestionListView.as_view(), name='random-question-list'),

    # 3. Проверить ответы и вернуть правильные
    path('questions/<int:pk>/check-answers/', CheckAnswersView.as_view(), name='check-answers'),
]
