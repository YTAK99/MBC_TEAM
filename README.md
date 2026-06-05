# 🎓 ClassQ

> **사용자 참여형 Q&A 플랫폼**
>
> 질문하고, 답변하고, 함께 해결하는 지식 공유 커뮤니티

---

## 📌 프로젝트 소개

ClassQ는 사용자들이 자유롭게 질문을 등록하고 답변을 작성하며 지식을 공유할 수 있는 Q&A 플랫폼입니다.

단순한 게시판이 아닌 질문 중심의 커뮤니티 구조를 제공하여 사용자 간의 소통과 정보 공유를 지원합니다.

---

## ✨ 주요 기능

### 👤 회원 관리

* 회원가입
* 로그인 / 로그아웃
* 사용자 정보 관리

### ❓ 질문 관리

* 질문 작성
* 질문 수정
* 질문 삭제
* 질문 목록 조회
* 질문 상세 조회

### 💬 답변 기능

* 답변 작성
* 답변 수정
* 답변 삭제

### 🗨️ 댓글 기능

* 질문 댓글 작성
* 답변 댓글 작성

### 🔍 검색 기능

* 제목 검색
* 내용 검색
* 작성자 검색

### 👍 추천 기능

* 질문 추천
* 답변 추천

---

## 🛠 기술 스택

| 구분              | 기술                    |
| --------------- | --------------------- |
| Backend         | Django 5              |
| Database        | SQLite3               |
| Frontend        | HTML, CSS, Bootstrap  |
| Authentication  | Django Authentication |
| Version Control | Git, GitHub           |
| Deployment      | Docker                |
| Network         | Cloudflare Tunnel     |

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

---

## 📂 프로젝트 구조

```text
PROJECT1/
│
├── common/          # 회원가입, 로그인
├── pybo/            # 질문, 답변, 댓글
├── templates/       # HTML 템플릿
├── static/          # CSS, JS, 이미지
├── config/          # Django 설정
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## 📸 주요 화면

### 메인 화면

![메인화면](./README_IMAGE/main.png)

---

### 질문 상세 화면

![질문상세](./README_IMAGE/detail.png)

---

### 질문 작성 화면

![질문작성](./README_IMAGE/create.png)

---

### 로그인 화면

![로그인](./README_IMAGE/login.png)

---

## 🐳 Docker 실행 방법

### 이미지 빌드

```bash
docker compose build
```

### 컨테이너 실행

```bash
docker compose up
```

### 백그라운드 실행

```bash
docker compose up -d
```

### 종료

```bash
docker compose down
```

---

## 🌐 외부 접속

Cloudflare Tunnel을 활용하여 별도의 포트 포워딩 없이 외부 네트워크에서도 서비스를 이용할 수 있도록 구성하였습니다.

```bash
cloudflared tunnel --url http://localhost:80
```

생성된 URL을 통해 모바일 및 외부 환경에서 접속 가능합니다.

---

## 🚀 개발 과정

### 구현 완료

* [x] 회원가입
* [x] 로그인 / 로그아웃
* [x] 질문 CRUD
* [x] 답변 CRUD
* [x] 댓글 기능
* [x] 추천 기능
* [x] 검색 기능
* [x] Docker 컨테이너화
* [x] Cloudflare Tunnel 연동

---

## 👥 팀원 역할

<!-- ### 한영탁

* 회원가입 및 로그인 구현
* 질문 상세 페이지 구현
* 댓글 기능 구현
* 검색 기능 구현
* Docker 환경 구성
* Cloudflare Tunnel 연동 및 테스트 -->

---

## 📖 기대 효과

* 자유로운 질문 및 답변 문화 형성
* 사용자 간 지식 공유 활성화
* 커뮤니티 기반 문제 해결 환경 제공
* 웹 서비스 개발 및 배포 경험 확보

---

## 📄 License

This project is created for educational purposes.
