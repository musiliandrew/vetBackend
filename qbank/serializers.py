from rest_framework import serializers
from .models import Subject, SubTopic, Chapter, Question, Option, UserProgress, QuestionInteraction

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'identifier', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    interaction = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'question_type', 'is_pyq', 'pyq_info', 'difficulty', 'options', 'interaction')

    def get_interaction(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            interaction = QuestionInteraction.objects.filter(user=user, question=obj).first()
            if interaction:
                return {
                    "is_bookmarked": interaction.is_bookmarked,
                    "is_liked": interaction.is_liked,
                    "is_reported": interaction.is_reported,
                    "user_note": interaction.user_note
                }
        return None

class ChapterSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'description', 'order', 'progress')

    def get_progress(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            progress = UserProgress.objects.filter(user=user, chapter=obj).first()
            if progress:
                return {
                    "attempted": progress.questions_attempted,
                    "correct": progress.questions_correct
                }
        return None

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ('id', 'title', 'description', 'order')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'title_en', 'title_hi', 'description', 'icon_identifier', 'order')
