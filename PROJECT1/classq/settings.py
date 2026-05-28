from pathlib import Path

# 프로젝트 기본 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 키
SECRET_KEY = "django-insecure-your-secret-key"

# 개발 모드
DEBUG = True

ALLOWED_HOSTS = []

# 설치 앱
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 앱
    "questions",
]

# 미들웨어
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL 설정
ROOT_URLCONF = "classq.urls"

# 템플릿 설정
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # templates 폴더 연결
        "DIRS": [BASE_DIR / "templates"],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "classq.wsgi.application"

# 데이터베이스
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 언어/시간
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

# 정적 파일(css/js/image)
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 로그인 설정
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

# 기본 PK 타입
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"