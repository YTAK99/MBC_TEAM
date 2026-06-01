from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("questions.urls", namespace="questions")),
]
handler404 = "questions.views.custom_404"