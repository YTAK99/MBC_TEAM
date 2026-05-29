# 화면 이동(render, redirect) 기능
from django.shortcuts import render, redirect

# 로그인 / 로그아웃 기능
from django.contrib.auth import logout, login

# 사용자(User) 모델
from django.contrib.auth.models import User

# 로그인한 사용자만 접근 가능하게 하는 기능
from django.contrib.auth.decorators import login_required

# JSON 형태 응답 기능
from django.http import JsonResponse

# 직접 만든 폼 가져오기
from .forms import QuestionForm, SignupForm

# Question 모델 가져오기
from .models import Question


# =========================
# 메인 페이지
# =========================
def home(request):

    # 최신 질문 5개 가져오기
    questions = Question.objects.all()[:5]

    # 전체 질문 개수
    question_count = Question.objects.count()

    # home.html 화면에 데이터 전달
    return render(
        request,
        "questions/home.html",
        {
            "questions": questions,
            "question_count": question_count,
        },
    )


# =========================
# 질문 게시판 페이지
# =========================
def board(request):

    # 모든 질문 가져오기
    questions = Question.objects.all()

    # board.html 화면 출력
    return render(
        request,
        "questions/board.html",
        {
            "questions": questions,
        },
    )


# =========================
# 질문 작성 페이지
# 로그인한 사용자만 접근 가능
# =========================
@login_required
def ask(request):

    # 사용자가 폼 제출했을 때
    if request.method == "POST":

        # 입력 데이터 저장
        form = QuestionForm(request.POST)

        # 입력값 검증 성공 시
        if form.is_valid():

            # 질문 생성
            Question.objects.create(

                # 작성자
                author=request.user,

                # 제목
                title=form.cleaned_data["title"],

                # 내용
                content=form.cleaned_data["content"],
            )

            # 게시판 페이지로 이동
            return redirect("questions:board")

    else:

        # GET 요청 시 빈 폼 생성
        form = QuestionForm()

    # ask.html 화면 출력
    return render(
        request,
        "questions/ask.html",
        {
            "form": form,
        },
    )


# =========================
# 질문 상세 페이지
# =========================
def detail(request, pk):

    # pk 번호에 해당하는 질문 가져오기
    question = Question.objects.get(pk=pk)

    # detail.html 화면 출력
    return render(
        request,
        "questions/detail.html",
        {
            "question": question,
        },
    )


# =========================
# 회원가입 기능
# =========================
def signup(request):

    # 회원가입 버튼 눌렀을 때
    if request.method == "POST":

        # 입력 데이터 저장
        form = SignupForm(request.POST)

        # 입력값 검증 성공 시
        if form.is_valid():

            # 사용자 생성
            user = form.save()

            # 회원가입 후 자동 로그인
            login(request, user)

            # 메인 페이지 이동
            return redirect("questions:home")

    else:

        # GET 요청 시 빈 회원가입 폼 생성
        form = SignupForm()

    # signup.html 화면 출력
    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
        },
    )


# =========================
# 로그아웃 기능
# =========================
def logout_view(request):

    # 현재 사용자 로그아웃
    logout(request)

    # 메인 페이지 이동
    return redirect("questions:home")


# =========================
# 아이디 중복 확인 기능
# =========================
def check_username(request):

    # 입력한 username 값 가져오기
    username = request.GET.get("username")

    # 이미 존재하는 아이디인지 검사
    exists = User.objects.filter(
        username=username
    ).exists()

    # JSON 형태로 결과 반환
    return JsonResponse({
        "exists": exists
    })

