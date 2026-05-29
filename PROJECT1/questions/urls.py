from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("ask/", views.ask, name="ask"),
    path("questions/<int:pk>/", views.detail, name="detail"),
    path("questions/<int:pk>/resolve/", views.resolve, name="resolve"),
    path("questions/<int:pk>/agree/", views.agree_toggle, name="agree"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("check-username/", views.check_username, name="check_username"),
    path("teacher/", views.teacher_home, name="teacher_home"),
    path("teacher/board/", views.teacher_question_list, name="teacher_board"),
]
