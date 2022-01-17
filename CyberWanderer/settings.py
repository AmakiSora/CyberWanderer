"""
CyberWanderer 项目的 Django 设置

由“django-admin startproject”使用 Django 3.2.8 生成。

有关此文件的更多信息，请参见
https://docs.djangoproject.com/en/3.2/topics/settings/

有关设置及其值的完整列表，请参阅
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from configparser import ConfigParser
from qiniu import *
import logging

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR为项目的绝对路径
from qiniu.services.storage import bucket

BASE_DIR = Path(__file__).resolve().parent.parent

# 引用外部配置文件
parser = ConfigParser()

# 配置文件路径
if os.path.exists(os.path.join(BASE_DIR, 'config_local.conf')):
    conf_path = os.path.join(BASE_DIR, 'config_local.conf')
    print('加载本地环境配置')
else:
    conf_path = os.path.join(BASE_DIR, 'config_pro.conf')
    print('加载线上环境配置')

# 读取配置文件
parser.read(conf_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&nf0_lqn0x+of6@fbe#x&vs^o#+86=xtv55^fz@musej3cai0u'

# SECURITY WARNING: don't run with debug turned on in production!
# 启动模式,
#   true为调试模式,检测到代码改动,立即重启服务,有报错页面
#   false为上线模式
DEBUG = parser.get('main', 'debug')

# 允许的请求头,没有以下参数不能通过
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twitter',  # 推特模块
    'translate',  # 翻译模块
    'bilibili',  # 批哩批哩模块
]
# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 主路由,一般不会变
ROOT_URLCONF = 'CyberWanderer.urls'

# 网页相关配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'CyberWanderer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': parser.get('mysql', 'name'),
        'USER': parser.get('mysql', 'user'),
        'PASSWORD': parser.get('mysql', 'password'),
        'HOST': parser.get('mysql', 'host'),
        'port': parser.get('mysql', 'port'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

# 用户密码加密
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# 修改语言
LANGUAGE_CODE = 'zh-hans'

# 设置时区(Linux中必须是Asia/Shanghai,windows中无所谓)
TIME_ZONE = 'Asia/Shanghai'

# 国际化
USE_I18N = True

# 本地化
USE_L10N = True

# 时区开关,true为utc时间,false为TIME_ZONE设置的时区
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "/static/",
#     # '/www/django/CyberWanderer/static/'
# ]
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '\033[0;32m {message} \033[0m',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console1': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console','console1'],
        'level': 'INFO',
    },
}

# 下载文件位置
DOWNLOAD_PATH = parser.get('main', 'downloadPath')

# 代理设置
PROXIES = {
    'http': parser.get('proxies', 'http'),
    'https': parser.get('proxies', 'https')
}

# 七牛云设置
QN = Auth(parser.get('qiniu', 'AccessKey'), parser.get('qiniu', 'SecretKey'))

# 百度翻译设置
BAIDU = {
    "appid": parser.get('baidu', 'appid'),
    "appkey": parser.get('baidu', 'appkey')
}
TENCENT = {
    'secret_id': parser.get('tencent', 'secret_id'),
    'secret_key': parser.get('tencent', 'secret_key'),
}
