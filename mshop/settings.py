"""
Django settings for mshop project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from alipay import AliPay

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hdbrwnl**8keu*ess9av+aqcq3v!$*b*8@9!(r5)95p!1=&r@@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'paypal.standard.ipn',
    'registration',
    'cart',
    'easy_thumbnails',
    'filer',
    'mptt',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
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

ROOT_URLCONF = 'mshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '/static/')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/Django20/mshop/media'

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',

    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 高分辨率
THUMBNAIL_HIGH_RESOLUTION = True
# 处理缩略图
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.filters',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
)
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': '/home/Django20/mshop/media/filter',
                'base_url': '/media/filter'
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': '/home/Django20/mshop/media/filer_thumbnails',
                'base_url': '/media/filer_thumbnails'
            },
        },
    },

}

# 邮箱发送短信
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
# 发送邮件的邮箱
EMAIL_HOST_USER = 'fangyingdon@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'NVAWJVGUEAPPNYBW'
# 打开ssl协议
EMAIL_USE_SSL = True

# EMAIL_USE_TLS = True
# # 收件人看到的发件人
EMAIL_FROM = '<fangyingdon@163.com>'
DEFAULT_FROM_EMAIL = 'fangyingdon@163.com'
# 设置session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# # 支付设置
# PAYPAL_TEST = True
# PAYPAL_REVEIVER_EMAIL = 'fangyingdon@163.com'
#
# PUBLIC_KEY = open(os.path.join(BASE_DIR, 'keys/alipay_public_key.pem'), 'r').read()
# PRIVATE_KEY = open(os.path.join(BASE_DIR, 'keys/app_private_key.pem'), 'r').read()
# alipay = AliPay(
#     appid="	2021000116688388",  # APPID
#     app_notify_url=None,  # 默认回调url
#     app_private_key_string=PRIVATE_KEY,
#     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#     # 支付宝的公钥是通过你自己的公钥验签之后生成的,
#     alipay_public_key_string=PUBLIC_KEY,
#     sign_type="RSA2",  # RSA 或者 RSA2
#     debug=False  # 默认False
# )
