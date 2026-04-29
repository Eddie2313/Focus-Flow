from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, FocusSession
from django.utils import timezone
from django.http import JsonResponse



def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "focus/register.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "focus/register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect("dashboard")

    return render(request, "focus/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "focus/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "focus/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    return render(request, "focus/dashboard.html")


@login_required
def timers(request):
    return render(request, "focus/timers.html")


@login_required
def tasks(request):
    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority")

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                priority=priority
            )

        return redirect("tasks")

    tasks = Task.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "focus/tasks.html", {
        "tasks": tasks
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("tasks")


@login_required
def stats(request):
    today = timezone.now().date()

    tasks_done = Task.objects.filter(
        user=request.user,
        completed=True
    ).count()

    today_sessions = FocusSession.objects.filter(
        user=request.user,
        completed_at__date=today
    )

    sessions_completed = today_sessions.count()

    total_focus_time = sum(session.minutes for session in today_sessions)

    return render(request, "focus/stats.html", {
        "tasks_done": tasks_done,
        "sessions_completed": sessions_completed,
        "total_focus_time": total_focus_time,
    })

@login_required
def complete_focus_session(request):
    if request.method == "POST":
        minutes = int(request.POST.get("minutes", 0))

        if minutes > 0:
            FocusSession.objects.create(
                user=request.user,
                minutes=minutes
            )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)
@login_required
def settings(request):
    return render(request, "focus/settings.html")