from rest_framework import serializers

from .models import Answer, Question, Subject


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
                  'question_count', 'question_time']

    def get_total_questions(self, obj):
        return obj.questions.count()
