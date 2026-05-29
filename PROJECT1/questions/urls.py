from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_page"),
    path("board/", views.board, name="board"),
    path("ask/", views.ask, name="ask"),
    # 질문 상세 및 상세 페이지에서 호출하는 POST 전용 액션
    path("questions/<int:pk>/", views.detail, name="detail"),           # GET·POST(답변 작성)
    path("questions/<int:pk>/resolve/", views.resolve, name="resolve"),  # POST: 해결됨 처리
    path("questions/<int:pk>/agree/", views.agree_toggle, name="agree"),  # POST: 공감 토글
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
]
