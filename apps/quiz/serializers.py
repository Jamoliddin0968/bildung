from rest_framework import serializers

from .models import Answer, AudioFile, Question, Subject


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
