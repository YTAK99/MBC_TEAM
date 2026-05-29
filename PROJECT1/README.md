# ClassQ — Django 버전 실행 가이드

## 프로젝트 소개

ClassQ

수업 중 질문과 답변을 관리하는 Q&A 플랫폼
학생 질문 등록
태그 기반 검색
답변 작성
해결 여부 관리
좋아요 기능

## 빠른 시작

```bash
# 1. 가상환경 생성 & 활성화
python -m venv venv
venv\Scripts\activate       # source venv/bin/activate 

# 2. 패키지 설치
pip install -r requirements.txt

* 위가 안되면 각각 실행
pip install django
pip install django-environ
pip install pillow

# 3. 환경변수 설정 (manage.py 가 있는 폴더에서)
copy .env.example .env

# .env 파일에서 SECRET_KEY를 실제 값으로 변경
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# .env 파일에서
SECRET_KEY=여기에_방금_생성한_키_붙여넣기 (따옴표없이)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

python manage.py check

# 4. DB 마이그레이션
python manage.py makemigrations accounts
python manage.py makemigrations questions
python manage.py migrate

안될때 del db.sqlite3하고 다시

# 5. 초기 태그 데이터 로드
python manage.py loaddata questions/fixtures/tags.json

# 6. 관리자 계정 생성
python manage.py createsuperuser

# 7. 개발 서버 실행
python manage.py runserver
```

브라우저에서 http://127.0.0.1:8000 접속

---



## 앱 구조 요약

| 파일 | 역할 |
|------|------|
| `accounts/models.py` | role(student/ta/instructor) 포함 CustomUser |
| `questions/models.py` | Tag, Question, Answer, Like |
| `questions/views.py` | Home, Board, Detail, Ask, Like(AJAX), Resolve |
| `questions/forms.py` | QuestionForm, AnswerForm |
| `templates/base.html` | 사이드바 + 탑바 공통 레이아웃 |

## URL 구조

```
/                       홈
/board/                 질문 목록 (검색, 태그 필터, 정렬)
/board/<id>/            질문 상세 + 답변
/ask/                   질문 등록 (로그인 필요)
/board/<id>/like/       좋아요 토글 POST → JSON
/board/<id>/resolve/    해결됨 표시 POST (작성자만)
/accounts/login/        로그인
/accounts/logout/       로그아웃
/accounts/signup/       회원가입
/admin/                 관리자 페이지
```

## 배포 시 추가 사항

1. `DEBUG=False` 설정
2. `SECRET_KEY` 강력한 랜덤값으로 교체
3. PostgreSQL로 전환 (`DATABASE_URL` 변경)
4. `python manage.py collectstatic` 실행
5. Tailwind CDN → CLI 빌드로 교체 (선택)
