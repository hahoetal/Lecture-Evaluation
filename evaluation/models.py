from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from lectures.models import Lectures
from accounts.models import User

class Evals(models.Model):
    num = models.AutoField(primary_key=True) # 글번호
    eval_date = models.DateTimeField() # 작성일자
    content = models.TextField() # 내용
    hw_level = models.IntegerField() # 과제 난이도
    test_level = models.IntegerField() # 시험 난이도
    lect_power = models.IntegerField() # 강의력
    counts = models.IntegerField(default=0) # 추천수
    lect_id = models.ForeignKey(Lectures, db_column="lect_id", on_delete=models.CASCADE)
    author = models.ForeignKey(User, db_column="author", on_delete=models.SET_NULL, blank=True, null=True) # 작성자

    class Meta:
        managed = False
        db_table = 'Evals'

    def __str__(self):
        return self.content[:10]

    def summary(self):
        return self.content[:40]

# class Evals(models.Model):
#     num = models.AutoField(primary_key=True) # 글번호
#     lect_id = models.ForeignKey(Lectures, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # 작성자
#     eval_date = models.DateTimeField() # 작성일자
#     content = models.TextField(null=False) # 내용
#     hw_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # 과제 난이도
#     test_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])# 시험 난이도
#     lect_power = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])# 강의력
#     # 수강학기
#     count = models.IntegerField(default=0) # 추천수

#     def __str__(self):
#         return self.content[:10]

#     def summary(self):
#         return self.content[:60]