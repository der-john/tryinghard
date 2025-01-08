import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
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
        raise Http404("Habit / Streak does not exist")
    return render(request, "habits/detail.html",
        { "habit": habit, "entry_dates": entry_dates, "yr": request.GET.get("yr"), "mo": request.GET.get("mo") })


def setentry(request, h_id):
    try:
        habit = Habit.objects.get(pk=h_id)
        year_str = request.POST["year"]
        month_str = request.POST["month"]
        day = int(request.POST["day"])
        e_date = datetime.date(int(year_str), int(month_str), day)
        entries = Entry.objects.filter(habit=habit).filter(date=e_date)

        if len(entries) == 0:
            new_entry = Entry.objects.create(habit=habit, date=e_date)
            Entry.save(new_entry)
        else:
            entries.delete()

    except Habit.DoesNotExist:
        raise Http404("Habit / Streak does not exist")
    return HttpResponseRedirect("/trh/" + str(h_id) + "?yr=" + year_str + "&mo=" + month_str)
