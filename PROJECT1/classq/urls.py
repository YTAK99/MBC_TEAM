from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # questions 앱
    path("", include("questions.urls", namespace="questions")),

    # Django 기본 로그인/로그아웃
    path("accounts/", include("django.contrib.auth.urls")),

    # allauth
    path("accounts/", include("allauth.urls")),
]
handler404 = "questions.views.custom_404"