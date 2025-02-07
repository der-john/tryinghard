from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import random
import string


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    default_title = 'New Challenge ' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    title = models.CharField(max_length=40, default=default_title)

    description = models.CharField(max_length=250, blank=True, default='')

    viewers = models.ManyToManyField(User, related_name="shared_habits")

    start_date = models.DateField("habit start date", default=timezone.now()) # TODO: Do something interesting with this

    is_intensity = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Entry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)

    date = models.DateField("date of entry", default=timezone.now())

    entry_text = models.CharField(max_length=400, blank=True, default='') # TODO: Do something interesting with this

    intensity = models.IntegerField(default=5, blank=True) # TODO: Do something interesting with this

    color = models.CharField(max_length=400, default='#008000')

    def __str__(self):
        return self.entry_text
