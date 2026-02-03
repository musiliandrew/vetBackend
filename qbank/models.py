from django.db import models
from django.conf import settings

class Subject(models.Model):
    title_en = models.CharField(max_length=255)
    title_hi = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    icon_identifier = models.CharField(max_length=50, help_text="Icon name mapping for frontend")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en

class SubTopic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subtopics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Chapter(models.Model):
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='MCQ')
    is_pyq = models.BooleanField(default=False)
    pyq_info = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. SSC 2024 Exam")
    difficulty = models.CharField(max_length=20, default='Medium') # Easy, Medium, Hard
    
    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    identifier = models.CharField(max_length=1) # A, B, C, D
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.identifier} - {self.text}"

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    questions_attempted = models.PositiveIntegerField(default=0)
    questions_correct = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter')

class QuestionInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_bookmarked = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    user_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'question')
