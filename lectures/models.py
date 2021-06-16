from django.db import models

# 강의 모델
class Lectures(models.Model):
    num = models.AutoField(primary_key=True) # 강의 번호, 교수님이 다르고 학수번호와 강의명이 동일한 강의가 존재
    lecture_name = models.TextField() # 강의명
    lecture_id = models.CharField(max_length=8) # 학수번호
    professor = models.TextField() # 교수명
    department = models.TextField() # 개설학과
    lecture_type = models.CharField(max_length=4) # 과목구분(전공, 교양, 교직 등)
    hit = models.IntegerField(default=0) # 강의 조회수
    lecture_plan = models.ImageField(upload_to="img", null=True, blank=True) # 강의계획서

    class Meta:
        managed = False
        db_table = 'Lectures'
    
    def __str__(self):
        return self.lecture_name
    

# class Lectures(models.Model):
#     num = models.AutoField(primary_key=True) # 강의 번호, 교수님이 다르고 학수번호와 강의명이 동일한 강의가 존재
#     lecture_name = models.TextField()   # 강의명
#     lecture_id = models.TextField()     # 학수번호
#     professor = models.TextField()      # 교수명
#     department = models.TextField()     # 개설학과
#     lecture_type = models.TextField()   # 과목구분(전공, 교양, 교직 등)
#     count = models.IntegerField(default=0) # 강의 조회수
#     lecture_plan = models.ImageField(upload_to="img", null=True, blank=True) # 강의계획서

#     def __str__(self):
#         return self.lecture_name