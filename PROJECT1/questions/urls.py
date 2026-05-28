from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("ask/", views.ask, name="ask"),
    path("questions/<int:pk>/", views.detail, name="detail"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    
    # 강사용 페이지 추가
    path("teacher/", views.teacher_home, name="teacher_home"),
    path("teacher/board/", views.teacher_question_list, name="teacher_board"),
]
