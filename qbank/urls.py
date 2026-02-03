from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, SubTopicViewSet, ChapterViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'subtopics', SubTopicViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
