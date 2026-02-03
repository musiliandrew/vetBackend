from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Subject, SubTopic, Chapter, Question, Option, UserProgress, QuestionInteraction
from .serializers import (
    SubjectSerializer, SubTopicSerializer, ChapterSerializer, 
    QuestionSerializer, OptionSerializer
)

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

class SubTopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            return SubTopic.objects.filter(subject_id=subject_id)
        return super().get_queryset()

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        subtopic_id = self.request.query_params.get('subtopic')
        if subtopic_id:
            return Chapter.objects.filter(sub_topic_id=subtopic_id)
        return super().get_queryset()

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chapter_id = self.request.query_params.get('chapter')
        is_bookmarked = self.request.query_params.get('bookmarked')
        is_pyq = self.request.query_params.get('pyq')
        
        queryset = Question.objects.all()
        
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        
        if is_pyq == 'true':
            queryset = queryset.filter(is_pyq=True)
            
        if is_bookmarked == 'true':
            queryset = queryset.filter(
                questioninteraction__user=self.request.user, 
                questioninteraction__is_bookmarked=True
            )
            
        return queryset

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        question = self.get_object()
        selected_option_id = request.data.get('option_id')
        is_correct = Option.objects.filter(id=selected_option_id, question=question, is_correct=True).exists()
        
        # Update progress
        progress, _ = UserProgress.objects.get_or_create(user=request.user, chapter=question.chapter)
        progress.questions_attempted += 1
        if is_correct:
            progress.questions_correct += 1
        progress.save()
        
        return Response({"is_correct": is_correct})

    @action(detail=True, methods=['post'])
    def toggle_bookmark(self, request, pk=None):
        question = self.get_object()
        interaction, _ = QuestionInteraction.objects.get_or_create(user=request.user, question=question)
        interaction.is_bookmarked = not interaction.is_bookmarked
        interaction.save()
        return Response({"is_bookmarked": interaction.is_bookmarked})
