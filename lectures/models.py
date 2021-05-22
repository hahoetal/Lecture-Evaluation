from django.db import models

# 강의 모델
class Lectures(models.Model):
    lecture_name = models.TextField(primary_key=True)   # 강의명
    lecture_id = models.TextField()     # 학수번호
    professor = models.TextField()      # 교수명
    department = models.TextField()     # 개설학과
    lecture_type = models.TextField()   # 과목구분(전공, 교양, 교직 등)

    class Meta:
        managed = False
        db_table = 'lectures'
        unique_together = (('lecture_id', 'professor')) # 두 colunm으로 row 구분