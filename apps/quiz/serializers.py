from typing import List
from rest_framework import serializers

from .models import Answer, AudioFile, BachelorProgram, Question, Subject


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'code', 'answers']


class SubjectSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'language', 'image',
                  'question_count', 'question_time', "total_questions"]

    def get_total_questions(self, obj):
        return obj.questions.count()


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class CustomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'subject', 'is_active']


class CustomSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'language']


class CustomAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'question', 'is_correct']


class SubjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Subject


class BachelorProgramSerializer(serializers.ModelSerializer):
    first_subject = SubjectShortSerializer()
    second_subject = SubjectShortSerializer()

    class Meta:
        model = BachelorProgram
        fields = "__all__"


class OnlyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("text",)
        model = Answer


class SubjectQuestionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        qs = obj.questions.all().order_by('?')[:30]
        return QuestionSerializer(qs, many=True).data

    class Meta:
        model = Subject
        fields = "__all__"


class RequiredSubjectQuestionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        qs = obj.questions.all().order_by('?')[:10]
        return QuestionSerializer(qs, many=True).data

    class Meta:
        model = Subject
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    def get_subjects(self, obj: BachelorProgram) -> List[RequiredSubjectQuestionSerializer]:
        data = []
        first_subject_data = SubjectQuestionSerializer(obj.first_subject).data
        first_subject_data['point'] = obj.first_subject_point
        data.append(first_subject_data)

        # Добавляем второй предмет и его баллы
        second_subject_data = SubjectQuestionSerializer(
            obj.second_subject).data
        second_subject_data['point'] = obj.second_subject_point
        data.append(second_subject_data)

        # Добавляем обязательные предметы и их баллы
        required_subject1_data = RequiredSubjectQuestionSerializer(
            obj.required_subject1).data
        required_subject1_data['point'] = obj.required_subject1_point
        data.append(required_subject1_data)

        required_subject2_data = RequiredSubjectQuestionSerializer(
            obj.required_subject2).data
        required_subject2_data['point'] = obj.required_subject2_point
        data.append(required_subject2_data)

        required_subject3_data = RequiredSubjectQuestionSerializer(
            obj.required_subject3).data
        required_subject3_data['point'] = obj.required_subject3_point
        data.append(required_subject3_data)

        return data

    class Meta:
        model = BachelorProgram
        fields = "__all__"
