from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginPage, name="loginPage"), # 로그인 페이지
    path('login', views.LoginView.as_view(), name="login"), # 로그인
    path('logout', views.userLogout, name="logout"), # 로그아웃
]