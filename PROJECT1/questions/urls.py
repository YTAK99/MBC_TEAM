# URL 연결 기능
from django.urls import path

# Django 기본 로그인 기능
from django.contrib.auth.views import LoginView

# 현재 폴더의 views.py 가져오기
from . import views


# 앱 이름 설정
app_name = "questions"


# URL 목록
urlpatterns = [

    # =========================
    # 메인 페이지
    # =========================
    path(
        "",
        views.home,
        name="home"
    ),

    # home/ 주소로 접속 시 메인 페이지 연결
    path(
        "home/",
        views.home,
        name="home_page"
    ),

    # =========================
    # 질문 게시판 페이지
    # =========================
    path(
        "board/",
        views.board,
        name="board"
    ),

    # =========================
    # 질문 작성 페이지
    # =========================
    path(
        "ask/",
        views.ask,
        name="ask"
    ),

    # =========================
    # 질문 상세 페이지
    # <int:pk> = 질문 번호
    # =========================
    path(
        "questions/<int:pk>/",
        views.detail,
        name="detail"
    ),

    # =========================
    # 로그인 페이지
    # Django 기본 LoginView 사용
    # =========================
    path(
        "login/",

        LoginView.as_view(

            # 사용할 로그인 HTML 파일
            template_name="registration/login.html"
        ),

        name="login",
    ),

    # =========================
    # 로그아웃 기능
    # =========================
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # =========================
    # 회원가입 페이지
    # =========================
    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    # =========================
    # 아이디 중복 확인 기능
    # AJAX 요청 처리
    # =========================
    path(
        "check-username/",

        views.check_username,

        name="check_username",
    ),
]
