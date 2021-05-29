from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"), # 로그인
    path('logout', views.userLogout, name="logout"), # 로그아웃
    path('signup', views.CreateUser.as_view(), name="signup"), # 회원가입
    path('find_id', views.find_id, name="findId"), # 아이디 찾기
    path('change_pw', views.change_pw, name="change_pw"), # 비밀번호 변경
    path('delete_user', views.delete_user, name="delete_user"), # 탈퇴하기
    path('mypage', views.mypage, name="mypage"), # mypage

    # 장고에서 지원하는 비밀번호 찾기 기능 사용하기_사용자가 가입 시 입력한 이메일을 이용.
    path('password_reset/', views.PWResetView.as_view(), name="password_reset"), # 비밀번호를 초기화할 수 있는 링크를 받을 이메일 작성 폼
    path('password_reset_done/', views.PWResetDoneView.as_view(), name="password_reset_done"), # 초기화 링크가 발송되고, 이를 알리는 페이지
    path('password_reset_confirm/<uidb64>/<token>/', views.PWResetConfirmView.as_view(), name="password_reset_confirm"), # 새로운 비밀번호를 입력하는 페이지
    path('password_reset_complete/', views.PWResetCompleteView.as_view(), name="password_reset_complete"), # 비밀번호 변경 완료를 알리는 페이지
]



# 장고에서 지원하는 비밀번호 찾기 기능 사용하기
# from django.contrib.auth import views as auth_views

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),