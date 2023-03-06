"""
Django settings for AIMeDocSys project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ttar_%7b)pane)#$-1ov(9!z!vt16h7*-*!&n!*hg8uw=wy4$f'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*"]
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # QQ邮箱的smtp服务器
EMAIL_PORT = 25  # 端口为465或587
# EMAIL_USE_SSL = True  # SSL加密方式设置为True
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '467807892@qq.com'  # 这里是你的邮箱账号
EMAIL_HOST_PASSWORD = 'jrlrljlzzhgzbhha'  # 注意这里不能用你邮箱账号的密码，而要用申请的设备授权码。
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# FUTURE_MAIL_SENDER = ('Future Admin', os.getenv('MAIL_USERNAME'))

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册haystack
    'haystack',
    # 注册rf
    'rest_framework',
    "medocsys.apps.MedocsysConfig"
]

# simpleui配置
SIMPLEUI_HOME_TITLE = '医道有易-后台管理'
SIMPLEUI_INDEX = '/chart/list/'
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = True
SIMPLEUI_HOME_QUICK = True
# 换成自己Logo链接
SIMPLEUI_LOGO = '/static/images/favicon/favicon.png'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 谁在前面先执行谁
    "medocsys.middleware.auth.LoginAuth",
]

ROOT_URLCONF = 'AIMeDocSys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AIMeDocSys.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aimedocsys',  # 数据库名
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': '127.0.0.1',  # 数据库主机地址
        'PORT': 3306,  # 数据库连接端口号
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  ## 新增行
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static').replace("\\", "/"),
# ]
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  ##修改地方
# ]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 允许使用内嵌iframe标签
X_FRAME_OPTIONS = 'SAMEORIGIN'
# 设置用户上传目录media目录
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# haystack配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'ENGINE': 'medocsys.elasticsearch_ik_backend.Elasticsearch7IkSearchEngine',
        'URL': 'http://127.0.0.1:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'doctxt',  # 指定elasticsearch建立的索引库的名称
        'EXCLUDED_INDEXES': ['medocsys.search_indexes.DocImgTxtIndex'],
    },
    'docimgtxt': {
        # 'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'ENGINE': 'medocsys.elasticsearch_ik_backend.Elasticsearch7IkSearchEngine',
        'URL': 'http://127.0.0.1:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'docimgtxt',  # 指定elasticsearch建立的索引库的名称
        'EXCLUDED_INDEXES': ['medocsys.search_indexes.DocTxtIndex'],
    },
}
# 搜索结果每页显示数量
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 3
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
