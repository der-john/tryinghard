from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)