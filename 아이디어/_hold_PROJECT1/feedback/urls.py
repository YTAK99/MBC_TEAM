from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),        # 메인 페이지
    path('sign-in/', views.signin, name='sign_in'),
]