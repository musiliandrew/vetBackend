from django.contrib import admin
from .models import Subject, SubTopic, Chapter, Question, Option, UserProgress, QuestionInteraction

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'order')

@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_topic', 'order')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'chapter', 'is_pyq', 'difficulty')
    inlines = [OptionInline]
    
    def text_preview(self, obj):
        return obj.text[:50]

admin.site.register(UserProgress)
admin.site.register(QuestionInteraction)
