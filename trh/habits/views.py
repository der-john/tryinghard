import datetime
import logging

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.template import loader

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Habit, Entry


def index(request, u_id):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    # The following will get more complicated after sharing
    if request.user.id != u_id:
        return HttpResponseForbidden()

    latest_streak_list = Habit.objects.filter(user=request.user).order_by("-start_date")[:5]
    template = loader.get_template("habits/index.html")
    context = {
        "latest_streak_list": latest_streak_list,
        "u_id": u_id
    }
    return HttpResponse(template.render(context, request))


def detail(request, u_id, h_id):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    # The following will get more complicated after sharing
    if request.user.id != u_id:
        return HttpResponseForbidden()

    try:
        nav_streak_list = Habit.objects.filter(user=request.user).exclude(id=h_id).order_by("-start_date")[:5]
        habit = Habit.objects.get(pk=h_id)
        entries = Entry.objects.filter(habit=habit)
        entry_dates = [[e.date.year, e.date.month, e.date.day] for e in entries]
    except Habit.DoesNotExist:
        raise Http404("Habit / Streak does not exist")
    return render(request, "habits/detail.html", {
            "u_id" : u_id,
            "habit": habit,
            "nav_streak_list": nav_streak_list,
            "entry_dates": entry_dates,
            "yr": request.GET.get("yr"),
            "mo": request.GET.get("mo")
        })


def setentry(request, u_id, h_id):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    # The following will get more complicated after sharing
    if request.user.id != u_id:
        return HttpResponseForbidden()

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
    return HttpResponseRedirect("/trh/" + str(u_id) + "/" + str(h_id) + "?yr=" + year_str + "&mo=" + month_str)


# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/trh/login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/trh/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            u_id = request.user.id
            return redirect('/trh/' + str(u_id))

    # Render the login page template (GET request)
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/trh/login/')