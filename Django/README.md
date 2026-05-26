# 깃 클론 후에 반드시 해야하는 것
- python -m venv venv
- venv/Scripts/activate
- pip install -r requirements.txt
- py manage.py makemigrations
- py manage.py migrate
- py manage.py runserver


# 모듈 추가 후 깃 커밋할때
- pip freeze > requirements.txt