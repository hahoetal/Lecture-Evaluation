# # csv 파일 읽어와 데이터베이스에 입력하기
# import os
# import django
# import csv
# import sys
# from .models import Lectures 

# os.environ.setdefault("DJANGO_SETTINGS_MODEULE", "Lecture-Evaluation.settings")
# django.setup()

# CSV_PATH_PRODUCTS='./lecture.csv'

# with open(CSV_PATH_PRODUCTS, delimeter=',') as csvfile:
#     data_reader = csv.DictReader(csvfile)

#     for row in data_reader:
#         print(row)
#         Lectures.objects.create(
#             lectureID = row['lectureID'],
#             lectureName = row['lectureName'],
#             professor = row['professor'],
#             lectureType = row['lectureType'],
#             department = row['department'],
#         )
