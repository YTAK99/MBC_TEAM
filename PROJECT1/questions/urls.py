from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("hall-of-fame/", views.hall_of_fame, name="hall_of_fame"),
    path("ask/", views.AskView.as_view(), name="ask"),  # 클래스 기반 코드는 반드시 뒤에 .as_view()를 붙여야함
    path("questions/<int:pk>/", views.detail, name="detail"),   # GET·POST(답변 작성)
    # 질문 상세 및 상세 페이지에서 호출하는 POST 전용 액션
    path("questions/<int:pk>/resolve/", views.resolve, name="resolve"),     # POST: 해결됨 처리
    path("questions/<int:pk>/agree/", views.agree_toggle, name="agree"),    # POST: 공감 토글
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("check-username/", views.check_username, name="check_username"),
    path("questions/<int:pk>/edit/", views.edit, name="edit"), # 질문 수정 페이지

    # 강사용 페이지 추가
    path("teacher/", views.teacher_home, name="teacher_home"),
    path("teacher/board/", views.teacher_question_list, name="teacher_board"),
]