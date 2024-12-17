from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader

from .models import Habit


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
    except Habit.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "habits/detail.html", {"habit": habit})