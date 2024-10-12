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


class ExamQuestionItemSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        fields = ("text", "answers")
        model = Question


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        pass
