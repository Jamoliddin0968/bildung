from django.contrib import admin
from .models import Subject, Question, Answer


class AnswerInline(admin.TabularInline):  
    model = Answer
    extra = 1  


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'code')
    inlines = [AnswerInline]  


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
