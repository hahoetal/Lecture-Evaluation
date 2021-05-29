from django.urls import path
from . import views

urlpatterns = [
    path("create_eval/<int:num>", views.create, name="create_eval"), # 강의평 작성하기, 강의 자세히 보기 페이지에 링크 연결
    path("delete_eval/<int:eval_id>", views.delete, name="delete_eval"), # 강의평 삭제하기
    path("recommand/<int:eval_num>/<int:lect_num>", views.recommand, name="recommand"), # 추천
]