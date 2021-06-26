# MySQL 사용하기
# mysql 서버가 현재 vmware 안에 있는 페도라에 깔려 있으니, vmware 열고 시작하기

# 필요한 패키지 설치
# pip install mysqlclient 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 사용할 엔진
        'NAME': 'projectdb', # 연동할 MySQL의 데이터베이스 이름
        'USER': 'root', # DB 접속 계정 이름
        'PASSWORD': 'onew1214', # DB 접속 계정 비밀번호
        'HOST': '192.168.242.129', # 실제 DB 주소, vmware 켜고 ipaddr 입력했을 때 나오는 ip 적어주기.
        'PORT': '3306', # SHOW GLOBAL VARIABLES LIKE 'PORT'; MySQL port 번호 찾기
    }
}

# DB 감지
# python manage.py inspectdb

# models.py에서 모델 수정
# 위 명령어를 입력하면 자동으로 mysql에 맞게 모델이 변환되어 출력되면 그대로 복사.
# DB와 table을 미리 만들어놓으면 됨.

# 모델이 변경되었으니 django에게 알려주기
# python manage.py makemigrations
# python manage.py migrate

# settings.py에 추가할 코드
# from . import my_settings
# DATABASES = my_settings.DATABASES



# 이메일 이용해서 비밀번호 찾기
# 장고에서 메일 보내기 위한 설정(smtp 프로토콜 사용)

# 네이버 메일
# 메일 환경 설정에 들어가서 POP3/IMAP 설정에서 '사용함'으로 체크
EMAIL ={
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS': 'True',
    'EMAIL_PORT': 587,
    'EMAIL_HOST': 'smtp.naver.com',
    'EMAIL_HOST_USER': 'duddms981220@naver.com',
    'EMAIL_HOST_PASSWORD': 'onew!1214',
    'SERVER_EMAIL': '',
}

# settings.py에 추가할 내용.
# EMAIL_BACKEND= my_settings.EMAIL['EMAIL_BACKEND']
# EMAIL_USE_TLS= my_settings.EMAIL['EMAIL_USE_TLS']
# EMAIL_PORT= my_settings.EMAIL['EMAIL_PORT']
# EMAIL_HOST= my_settings.EMAIL['EMAIL_HOST']
# EMAIL_HOST_USER= my_settings.EMAIL['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD= my_settings.EMAIL['EMAIL_HOST_PASSWORD']
# SERVER_EMAIL= my_settings.EMAIL['SERVER_EMAIL']
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER # 사이트와 관련한 자동응답을 받을 이메일 주소