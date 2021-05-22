from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LectureListPage, name="lectureList"), # 강의 목록 페이지 : ~lectures/
    path('search', views.serachLecture, name="searchLecture") # 강의 검색 결과 : ~lectures/search
]