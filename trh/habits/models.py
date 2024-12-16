import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    description = models.CharField(max_length=200)
    start_date = models.DateField("challenge start date")

    def __str__(self):
        return self.description


class Entry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    entry_text = models.CharField(max_length=200)
    intensity = models.IntegerField(default=5)
    def __str__(self):
        return self.entry_text
