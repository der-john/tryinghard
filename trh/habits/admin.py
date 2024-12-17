from django.contrib import admin

from .models import Entry, Habit

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1

class HabitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["start_date"]}),
        ("Habit Information",
            {"fields": ["title", "description", "is_multi_entry_day", "is_intensity"],
             "classes": ["collapse"]}),
    ]
    inlines = [EntryInline]

admin.site.register(Habit, HabitAdmin)