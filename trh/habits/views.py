from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader

from .models import Habit, Entry


def index(request):
    latest_streak_list = Habit.objects.order_by("-start_date")[:5]
    template = loader.get_template("habits/index.html")
    context = {
        "latest_streak_list": latest_streak_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, h_id):
    try:
        habit = Habit.objects.get(pk=h_id)
        entries = Entry.objects.filter(habit=habit)
        entry_dates = [[e.date.year, e.date.month, e.date.day] for e in entries]
    except Habit.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "habits/detail.html",
                  { "habit": habit,
                    "entry_dates": entry_dates
                   })