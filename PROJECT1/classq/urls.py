from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # questions 앱
    path("", include("questions.urls", namespace="questions")),

    # 로그인/로그아웃
    path("accounts/", include("django.contrib.auth.urls")),
]