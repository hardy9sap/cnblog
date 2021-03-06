"""
Django settings for cnblog project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1^^^c(hks*2&k$0!u+)fj)t!47qt1jxle%gw63763z7g1#^z^i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cnblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cnblog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cnblog',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': ''
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 静态文件  --》 特指服务器用到的文件
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 媒体静态文件 --》 用户用到的文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 自定义的并且继承了AbstractUser类的类，需要以下声明
AUTH_USER_MODEL = 'blog.UserInfo'

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

LOGIN_URL = "/login/"

# 邮件
# 邮件发送配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 这个可以不设置，是默认的
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465

# 发送邮件的邮箱
EMAIL_HOST_USER = 'hardy9sap@163.com'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = 'hardy9sap972600'
EMAIL_USE_SSL = True
"""
备注：
send_mail 每次发邮件都会建立一个连接，发多封邮件时建立多个连接。
而 send_mass_mail 是建立单个连接发送多封邮件，
所以一次性发送多封邮件时 send_mass_mail 要优于 send_mail。
from django.core.mail import send_mass_mail

message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])

send_mass_mail((message1, message2), fail_silently=False)

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'#这个可以不设置，是默认的
EMAIL_HOST = "smtp.sina.com"#用来发送邮件的主机
EMAIL_PORT = 25#默认主机端口，如果开启ssl或者tls（只能选一个）要改变端口
EMAIL_HOST_USER = "+++++@sina.com" # 你的邮箱账号
EMAIL_HOST_PASSWORD = "++++++" # 你的邮箱密码
EMAIL_USE_TLS = True # 和SMTP对话是否使用TLS安全连接端口587
EMAIL_USE_SSL = True # 和SMTP对话是否使用SSL安全连接端口465
EMAIL_FROM = "charlesval@sina.com"  # 你的邮箱账号
EMAIL_TIMEOUT=10#指定堵塞超时时间
       ssl使用的端口和取消ssl的端口不一样

       smtp   默认25         465(ssl)

       pop3   默认110       995(ssl)

       imap   默认143       993(ssl)

　　SSL协议提供的服务主要有：

　　1）认证用户和服务器，确保数据发送到正确的客户机和服务器；

　　2）加密数据以防止数据中途被窃取；

　　3）维护数据的完整性，确保数据在传输过程中不被改变。
--------------------- 
作者：李岳阳LYY 
来源：CSDN 
原文：https://blog.csdn.net/weixin_42557907/article/details/82290924 
版权声明：本文为博主原创文章，转载请附上博文链接！
"""
