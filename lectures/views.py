from django.shortcuts import render
from django.db.models import Q
from .models import Lectures
from django.contrib import messages

# 강의 목록 페이지 띄우기
def LectureListPage(request):
    lectures = Lectures.objects.all()
    return render(request, 'LectureList.html', {'lectures':lectures}) # lectures의 정보를 LectureList.html로 전달

# 강의 검색
def searchLecture(request):
    lectures = Lectures.objects.all().order_by('lecture_id') # Lectures의 모든 객체 가져오기(학수번호로 오름차순)
    
    # 검색어 가져오기
    search_lecture = request.POST.get('search_lecture') # 입력한 강의명(LectureList의 search_lecture) 가져오기
    search_major = request.POST.get('search_major') # 입력한 학과(LectureList의 search_major) 가져오기
    search_professor = request.POST.get('search_professor') # 입력한 교수명(LectureList의 search_professor) 가져오기
    search_type = request.POST.get('search_type')   # 입력한 과목구분(LectureList의 search_type) 가져오기

    # 4가지 중 하나라도 입력이 안됐다면 메세지 띄우기
    allNone = search_lecture == "" and search_major == "None" and search_professor == "" and search_type == "None"
    if(allNone):
        messages.warning(request, "강의명, 개설학과, 교수명, 과목구분 중 한 가지 항목은 필수입력 항목입니다.")
        return render(request, 'search_fail.html')

    # 조건 하나씩 검사하기
    if(search_lecture != ""):
        lectures = lectures.filter(Q(lecture_name__contains=search_lecture))
    if(search_major != "None"):
        lectures = lectures.filter(Q(department=search_major))
    if(search_professor != ""):
        lectures = lectures.filter(Q(professor__contains=search_professor))
    if(search_type != "None"): 
        lectures = lectures.filter(Q(lecture_type=search_type))

    return render(request, 'search.html', {'lectures' : lectures})