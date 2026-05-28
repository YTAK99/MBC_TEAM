from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("ask/", views.AskView.as_view(), name="ask"),  # 클래스 기반 코드는 반드시 뒤에 .as_view()를 붙여야함함
    path("questions/<int:pk>/", views.detail, name="detail"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
]
