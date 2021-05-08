from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginPage, name="loginPage"), # 로그인 페이지
    path('login', views.LoginView.as_view(), name="login"), # 로그인
    path('logout', views.userLogout, name="logout"), # 로그아웃
    path('signup', views.CreateUser.as_view(), name="signup"), # 회원가입
    path('find_id', views.find_id, name="findId"), # 아이디 찾기
    path('change_pw', views.change_pw, name="change_pw"), # 비밀번호 변경
]