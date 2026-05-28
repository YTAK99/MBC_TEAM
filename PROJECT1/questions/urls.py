from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("ask/", views.ask, name="ask"),
    path("questions/<int:pk>/", views.detail, name="detail"),

    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path("logout/", views.logout_view, name="logout"),

    path("signup/", views.signup, name="signup"),

    path(
        "check-username/",
        views.check_username,
        name="check_username",
    ),
]