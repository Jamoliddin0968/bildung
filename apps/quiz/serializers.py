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
    first_subject = SubjectQuestionSerializer()
    second_subject = SubjectQuestionSerializer()
    required_subject1 = RequiredSubjectQuestionSerializer()
    required_subject2 = RequiredSubjectQuestionSerializer()
    required_subject3 = RequiredSubjectQuestionSerializer()

    class Meta:
        model = BachelorProgram
        fields = "__all__"
