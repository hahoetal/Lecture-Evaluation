from django.urls import path
from . import views

urlpatterns = [
    path('', views.LectureListPage, name="lectureList"), # 강의 목록 페이지 : ~lectures/
    path('search_result', views.searchLecture, name="searchLecture"), # 강의 검색 결과 : ~lectures/search   
    path('detail/<int:lect_id>', views.detail, name="detail"), # 강의 자세히 보기
]