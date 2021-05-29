# django에서 제공하는 유저 모델 커스텀하기
import os
from django.conf import settings

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .choice import *

# 유저를 생성할 때 사용하는 Helper 클래스
class UserManager(BaseUserManager):
    def create_user(self, userId, major, studentId, email, password=None):
        if not userId:
            raise ValueError("아이디를 입력해주세요.")
        user = self.model(
            userId = userId,
            major = major,
            studentId = studentId,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userId, major, studentId, email, password=None):
        user = self.create_user(
            userId,
            password = password,
            major = major,
            studentId = studentId,
            email = email,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

# 유저 모델
class User(AbstractBaseUser):
    userId = models.CharField(
        verbose_name= 'User ID',
        max_length=12,
        unique=True,
        primary_key= True
    )

    major = models.CharField(max_length=15, choices=MAJOR_CHOICES, default="국어국문학과") # 개발자가 미리 만들어둔 보기 중에서 선택하도록!!
    studentId = models.CharField(unique=True, max_length=8)
    email = models.EmailField(max_length=255, unique=True)

    is_active= models.BooleanField(default= True) # django 유저 모델의 필수 필드_1
    is_admin= models.BooleanField(default= False) # django 유저 모델의 필수 필드_2

    objects = UserManager()

    USERNAME_FIELD = 'userId' # username 필드를 teacherID로 사용!
    REQUIRED_FIELDS = ['major', 'studentId', 'email']

    def __str__(self):
        return str(self.userId)
    # 이걸 적어주지 않으면, admin 사이트에서 사용자(객체) 목록이 object(1), object(2) 이런 식으로 떠서 뭐가 뭔지 알아보기 힘듦.

    # 아래 세 개는 커스텀한 유저 모델을 기본 유저 모델로 사용하기 위해 구현해야 하는 부분.
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
        # True가 반환되면 관리자 화면에 로그인할 수 있는 권한이 주어짐.