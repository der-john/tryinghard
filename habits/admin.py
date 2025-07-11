from django.contrib import admin

from .models import Entry, Habit

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1

class HabitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "title", "description", "start_date", "viewers", "is_intensity"]}),
    ]
    inlines = [EntryInline]

admin.site.register(Habit, HabitAdmin)