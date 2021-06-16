# django에서 제공하는 유저 모델 커스텀하기
import os
from django.conf import settings

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .choice import *

# 유저를 생성할 때 사용하는 Helper 클래스
class UserManager(BaseUserManager):
    def create_user(self, user_id, major, student_id, email, password=None):
        if not user_id:
            raise ValueError("아이디를 입력해주세요.")
        user = self.model(
            user_id = user_id,
            major = major,
            student_id = student_id,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, major, student_id, email, password=None):
        user = self.create_user(
            user_id,
            password = password,
            major = major,
            student_id = student_id,
            email = email,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

# class User(AbstractBaseUser):
#     user_id = models.CharField(
#         verbose_name= 'User ID',
#         max_length=12,
#         unique=True,
#         primary_key= True
#     )

#     major = models.CharField(max_length=15, choices=MAJOR_CHOICES, default="국어국문학과") # 개발자가 미리 만들어둔 보기 중에서 선택하도록!!
#     student_id = models.CharField(unique=True, max_length=8)
#     email = models.EmailField(max_length=255, unique=True)

#     is_active= models.BooleanField(default= True) # django 유저 모델의 필수 필드_1
#     is_admin= models.BooleanField(default= False) # django 유저 모델의 필수 필드_2

#     objects = UserManager()

#     USERNAME_FIELD = 'user_id' # username 필드를 teacherID로 사용!
#     REQUIRED_FIELDS = ['major', 'student_id', 'email']

#     def __str__(self):
#         return str(self.user_id)
#     # 이걸 적어주지 않으면, admin 사이트에서 사용자(객체) 목록이 object(1), object(2) 이런 식으로 떠서 뭐가 뭔지 알아보기 힘듦.

#     # 아래 세 개는 커스텀한 유저 모델을 기본 유저 모델로 사용하기 위해 구현해야 하는 부분.
    
#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
    
#     @property
#     def is_staff(self):
#         return self.is_admin
#         # True가 반환되면 관리자 화면에 로그인할 수 있는 권한이 주어짐.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class User(AbstractBaseUser):
    user_id = models.CharField(primary_key=True, max_length=12)
    major = models.CharField(max_length=15, choices=MAJOR_CHOICES, default="국어국문학과")
    student_id = models.CharField(unique=True, max_length=8)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.IntegerField(blank=True, null=True, default=1)
    is_admin = models.IntegerField(blank=True, null=True, default=0)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'

    objects = UserManager()
    
    USERNAME_FIELD = 'user_id' # username 필드를 userid로 사용!
    REQUIRED_FIELDS = ['major', 'student_id', 'email']

    def __str__(self):
        return str(self.user_id)

    # 아래 세 개는 커스텀한 유저 모델을 기본 유저 모델로 사용하기 위해 구현해야 하는 부분.
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
        # True가 반환되면 관리자 화면에 로그인할 수 있는 권한이 주어짐.