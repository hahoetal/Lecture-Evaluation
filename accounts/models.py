# django에서 제공하는 유저 모델 커스텀하기
import os
from django.conf import settings

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# 유저를 생성할 때 사용하는 Helper 클래스
class UserManager(BaseUserManager):
    def create_user(self, userId, major, studentId, email, password=None):
        if not userId:
            raise ValueError("회원 가입한 사람만 이용 가능한 서비스입니다.")
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
    )
    major = models.CharField(max_length=10) # 나중에 여러 보기 중 선택하는 것으로 바꾸기
    studentId = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    is_active= models.BooleanField(default= True) # django 유저 모델의 필수 필드_1
    is_admin= models.BooleanField(default= False) # django 유저 모델의 필수 필드_2

    objects = UserManager()

    USERNAME_FIELD = 'userId' # username 필드를 teacherID로 사용!
    REQUIRED_FIELDS = ['major', 'studentId', 'email']

    def __str__(self):
        return str(self.userId)

    # 아래 세 개는 커스텀한 유저 모델을 기본 유저 모델로 사용하기 위해 구현해야 하는 부분.
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
        # True가 반환되면 관리자 화면에 로그인할 수 있는 권한이 주어짐.