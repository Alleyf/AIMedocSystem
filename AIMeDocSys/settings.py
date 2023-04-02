"""
Django settings for AIMeDocSys project.
"""
import os
import mimetypes
from pathlib import Path

from py2neo import Graph

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ttar_%7b)pane)#$-1ov(9!z!vt16h7*-*!&n!*hg8uw=wy4$f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# 错误视图设置
# 部署环境静态路径配置
# 部署时使用collastic_static指令迁移静态文件
# STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 这里可以根据实际情况来定义，比如可以将static名修改
STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other
    'compressor.finders.CompressorFinder',
)

# 压缩器配置
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    # creates absolute urls from relative ones
    'compressor.filters.css_default.CssAbsoluteFilter',
    # css minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

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
    'drf_haystack',
    "medocsys.apps.MedocsysConfig",
    'compressor',
    'corsheaders',  # 跨域
    # 'jsonrpc',  # RPC服务
    # 'rest_framework_swagger',  # swagger自动生成接口文档

]

# neo4j配置
#                           ip地址     端口         neo4j账号   密码
graph = Graph("bolt://47.120.0.133:7687", auth=("neo4j", "password"))  # 连接neo4j图数据库

# simpleui配置
SIMPLEUI_HOME_TITLE = '智检慧医-后台管理'
SIMPLEUI_INDEX = '/chart/list/'
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = True
SIMPLEUI_HOME_QUICK = True
# 换成自己Logo链接
SIMPLEUI_LOGO = '/static/images/favicon/favicon.png'

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 谁在前面先执行谁
    'django.middleware.gzip.GZipMiddleware',
    "medocsys.middleware.auth.LoginAuth",
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]
# 缓存配置
# CACHE_MIDDLEWARE_ALIAS = "all_cache"
CACHE_MIDDLEWARE_SECONDS = 60 * 10
CACHE_MIDDLEWARE_KEY_PREFIX = ''

ROOT_URLCONF = 'AIMeDocSys.urls'

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

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

WSGI_APPLICATION = 'AIMeDocSys.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aimedocsys',  # 数据库名
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': '127.0.0.1',  # 数据库主机地址
        # 'HOST': 'db',  # 部署数据库主机地址
        'PORT': 3306,  # 数据库连接端口号
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://47.120.0.133:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 300},
            # "DECODE_RESPONSES": True,
            "PASSWORD": "medocsys",
        },
    },
}

REDIS_TIMEOUT = 7 * 24 * 60 * 60
CUBES_REDIS_TIMEOUT = 60 * 60
NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60

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

LANGUAGE_CODE = "zh-hans"

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

USE_I18N = True
# USE_I18N = False

USE_L10N = True

# USE_TZ = True

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
        # 'URL': 'http://43.139.217.160:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'doctxt',  # 指定elasticsearch建立的索引库的名称
        'EXCLUDED_INDEXES': ['medocsys.search_indexes.DocImgTxtIndex'],
    },
    'docimgtxt': {
        # 'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'ENGINE': 'medocsys.elasticsearch_ik_backend.Elasticsearch7IkSearchEngine',
        'URL': 'http://127.0.0.1:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        # 'URL': 'http://43.139.217.160:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'docimgtxt',  # 指定elasticsearch建立的索引库的名称
        'EXCLUDED_INDEXES': ['medocsys.search_indexes.DocTxtIndex'],
    },
}
# 搜索结果每页显示数量
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 3
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 在settings.py末尾加入,保证部署环境下静态文件正常加载
# SECURE_CONTENT_TYPE_NOSNIFF = False

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
