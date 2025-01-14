import datetime
import urllib.parse

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
    shared_streak_list = request.user.shared_habits.all()

    template = loader.get_template("habits/index.html")
    context = {
        "latest_streak_list": latest_streak_list,
        "shared_streak_list": shared_streak_list,
        "u_id": u_id
    }
    return HttpResponse(template.render(context, request))


def detail(request, u_id, h_id):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    habit = Habit.objects.get(pk=h_id)
    if request.user.id != u_id and request.user not in habit.viewers.all():
        return HttpResponseForbidden()

    try:
        nav_streak_list = Habit.objects.filter(user=request.user).exclude(id=h_id).order_by("-start_date")[:5]
        entries = Entry.objects.filter(habit=habit).order_by("date")
        entry_dates = [[e.date.year, e.date.month, e.date.day] for e in entries]
        entry_colors = [e.color for e in entries]
    except Habit.DoesNotExist:
        raise Http404("Habit / Streak does not exist")
    return render(request, "habits/detail.html", {
            "u_id" : request.user.id,
            "habit": habit,
            "is_viewer": request.GET.get("is_viewer"),
            "nav_streak_list": nav_streak_list,
            "entry_dates": entry_dates,
            "entry_colors": entry_colors,
            "yr": request.GET.get("yr"),
            "mo": request.GET.get("mo"),
            "entry_color": request.GET.get("color")
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

        color = urllib.parse.unquote(request.POST["color"])

        entries = Entry.objects.filter(habit=habit).filter(date=e_date)

        if len(entries) == 0:
            new_entry = Entry.objects.create(habit=habit, date=e_date, color=color)
            Entry.save(new_entry)
        else:
            entries.delete()

    except Habit.DoesNotExist:
        raise Http404("Habit / Streak does not exist")

    color_param = urllib.parse.quote(color)
    return HttpResponseRedirect(
        "/trh/" + str(u_id) + "/" + str(h_id) + "?yr=" + year_str + "&mo=" + month_str + "&color=" + color_param)


def create(request, u_id):
 
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    # The following will get more complicated after sharing
    if request.user.id != u_id:
        return HttpResponseForbidden()

    if request.method == "POST":
        hname = request.POST.get('hname')
        hdescription = request.POST.get('hdescription')

        if request.POST.get('hstartdate'):
            start_date = request.POST.get('hstartdate')
            new_habit = Habit.objects.create(
                user=request.user, title=hname, description=hdescription, start_date=start_date)
        else:
            new_habit = Habit.objects.create(user=request.user, title=hname, description=hdescription)
        Habit.save(new_habit)
        h_id = new_habit.id
        return redirect('/trh/' + str(u_id) + "/" + str(h_id) + "/?color=%23008000")

    # Render the create page template (GET request)
    return render(request, 'habits/create.html', { "u_id" : u_id })


def share(request, u_id):
 
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.user.id != u_id:
        return HttpResponseForbidden()

    if request.method == "POST":
        h_id = request.POST.get('habitId')
        viewer_id = request.POST.get('viewerId')
        viewer = User.objects.get(id=viewer_id)
        Habit.objects.get(pk=h_id).viewers.add(viewer)

        return redirect('/trh/' + str(u_id) + "/" + str(h_id) + "/?color=%23008000")

    # Render the share page template (GET request)
    h_id = request.GET.get('h_id')
    current_habit = Habit.objects.get(pk=h_id)
    users = User.objects.exclude(id=u_id)
    habits = Habit.objects.filter(user=request.user).exclude(id=h_id).order_by("-start_date")[:5]
    return render(request, 'habits/share.html',
        { "u_id" : u_id, "current_habit" : current_habit, "users" : users, "habits" : habits })


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