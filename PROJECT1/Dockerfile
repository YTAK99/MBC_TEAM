# Python 이미지
FROM python:3.12-slim-bookworm

# 작업 디렉토리
WORKDIR /app

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# requirements 먼저 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 프로젝트 복사
COPY . .

CMD sh -c "python manage.py migrate && \
           python manage.py seed && \
           python manage.py collectstatic --noinput && \
           gunicorn classq.wsgi:application --bind 0.0.0.0:8000"