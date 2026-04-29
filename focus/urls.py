from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("timers/", views.timers, name="timers"),
    path("tasks/", views.tasks, name="tasks"),
    path("stats/", views.stats, name="stats"),
    path("settings/", views.settings, name="settings"),
    path("tasks/complete/<int:task_id>/", views.complete_task, name="complete_task"),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("complete-focus-session/", views.complete_focus_session, name="complete_focus_session"),
]
