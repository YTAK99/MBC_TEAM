# ClassQ 프로젝트 구조

현재 구조는 `questions` 앱 하나만 활성화한 초기 학습용 구조입니다.

```txt
classq/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── classq/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── questions/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── questions/
│   │   ├── home.html
│   │   ├── board.html
│   │   ├── detail.html
│   │   └── ask.html
│   └── registration/
│       ├── login.html
│       └── signup.html
└── static/
    └── css/
        ├── classq-base.css
        ├── classq-home.css
        ├── classq-board.css
        ├── classq-detail.css
        └── classq-form.css
```

## 역할

- `classq`: 프로젝트 설정과 전체 URL 연결
- `questions`: 질문 서비스 화면, 최소 모델, 최소 폼
- `templates`: Django 템플릿 구조
- `static/css`: 분리된 CSS

## ERD 기준 최소 모델

- `Question`
- `Response`
- `Tag`
- `QuestionAgree`

기능 완성 로직은 넣지 않고, 이후 팀원이 직접 구현할 수 있는 이름과 구조만 남긴 상태입니다.
