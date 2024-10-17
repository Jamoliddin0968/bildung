from django import forms
from django.contrib import admin

from .models import Answer, BachelorProgram, Question, Subject


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    max_num = 4
    min_num = 4


@admin.register(BachelorProgram)
class BachelorProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'first_subject', 'second_subject')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'language')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'code')
    inlines = [AnswerInline]
    list_filter = ['subject', 'is_active']
    search_fields = ('code',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
