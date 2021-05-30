from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from lectures.models import Lectures
from accounts.models import User

class Evals(models.Model):
    num = models.AutoField(primary_key=True) # 글번호
    lect_id = models.ForeignKey(Lectures, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # 작성자
    # author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="알 수 없음") # 작성자
    date = models.DateTimeField() # 작성일자
    content = models.TextField(null=False) # 내용
    hw_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # 과제 난이도
    test_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])# 시험 난이도
    lect_power = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])# 강의력
    # 수강학기
    count = models.IntegerField(default=0) # 추천수

    def __str__(self):
        return self.content[:10]

    def summary(self):
        return self.content[:30]