# 깃 클론 후에 반드시 세팅해야하는 환경
- python -m venv venv
- venv/Scripts/activate
- pip install -r requirements.txt
- py manage.py makemigrations
- py manage.py migrate
- py manage.py createsuperuser
- py manage.py runserver


# 깃허브 변경 사항 당겨오려면 (커서 터미널에서)
- git pull

# 모듈 추가 후 깃 커밋할때
- pip freeze > requirements.txt


## 프로젝트 생성할때 터미널에 쓴 내용
- py -m venv venv
- cd venv/Scripts
- activate
- cd ../..
- pip install -r requirements.txt
- django-admin startproject config .
(프로젝트 이름은 실제 서비스명이 아니라 설정 폴더 느낌이라 config, core 많이 씀)
- py manage.py startapp feedback
- py manage.py makemigrations
- py manage.py migrate
- py manage.py createsuperuser
- py manage.py runserver