from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import QuestionForm, SignupForm, ResponseForm
from .models import Question, QuestionAgree, Response


def _login_redirect(request):
    """로그인 후 원래 페이지로 돌아가도록 next 에 현재 URL 을 담아 리다이렉트."""
    return redirect_to_login(request.get_full_path())

def home(request):              # 홈 페이지
    return render(request, "questions/home.html")


def board(request):             # 질문 목록 페이지
    return render(request, "questions/board.html")


def ask(request):               # 질문/추가답변 생성 페이지
    # 질문 작성은 로그인 사용자만 허용
    if not request.user.is_authenticated:
        return _login_redirect(request)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 현재 로그인 사용자를 작성자로 저장
            question.save()
            form.save_m2m()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "questions/ask.html", {"form": form})


def detail(request, pk):
    """
    질문 상세 페이지.
    - GET: 질문·답변 목록·답변 폼 표시
    - POST: 같은 URL 에서 Response 저장 (PRG 패턴으로 redirect)
    """
    # author/tags/agree_count 를 한 번에 조회해 N+1 방지
    question = get_object_or_404(
        Question.objects.select_related("author")
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees", distinct=True)),
        pk=pk,
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return _login_redirect(request)

        # 해결됨(RESOLVED) 질문에는 답변 작성 불가
        if question.is_resolved:
            return redirect("questions:detail", pk=pk)

        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.question = question
            response.author = request.user
            # 강사 계정은 ANSWER, 일반 사용자는 FOLLOW_UP 으로 구분 저장
            if request.user.is_staff:
                response.response_type = Response.ResponseType.ANSWER
            else:
                response.response_type = Response.ResponseType.FOLLOW_UP
            response.save()
            return redirect("questions:detail", pk=pk)
    else:
        form = ResponseForm()

    responses = question.responses.select_related("author").all()

    # 현재 사용자가 이미 '나도 궁금해요'를 눌렀는지 (버튼 스타일용)
    user_agreed = False
    if request.user.is_authenticated:
        user_agreed = QuestionAgree.objects.filter(
            question=question,
            user=request.user,
        ).exists()

    context = {
        "question": question,
        "form": form,
        "responses": responses,
        "user_agreed": user_agreed,
        "agree_count": question.agree_count,
    }
    return render(request, "questions/detail.html", context)


def resolve(request, pk):       # 질문 해결 처리
    """
    질문 작성자 본인만 상태를 RESOLVED 로 변경할 수 있다.
    버튼 오동작 방지를 위해 POST 요청만 허용한다.
    """
    if request.method != "POST":
        return redirect("questions:detail", pk=pk)

    question = get_object_or_404(Question, pk=pk)
    if not request.user.is_authenticated:
        return _login_redirect(request)

    # 작성자 본인일 때만 해결됨 처리
    if question.author_id == request.user.id:
        question.status = Question.Status.RESOLVED
        question.save(update_fields=["status"])

    return redirect("questions:detail", pk=pk)


def agree_toggle(request, pk):  # 질문 도움돼요(공감) 토글
    """
    로그인 사용자가 질문에 '도움돼요'를 누르면 공감이 추가되고,
    이미 누른 상태에서 다시 누르면 취소된다.
    """
    if request.method != "POST":
        return redirect("questions:detail", pk=pk)

    if not request.user.is_authenticated:
        return _login_redirect(request)

    question = get_object_or_404(Question, pk=pk)
    agree, created = QuestionAgree.objects.get_or_create(
        question=question,
        user=request.user,
    )
    if not created:
        agree.delete()

    return redirect("questions:detail", pk=pk)


def signup(request):            # 회원가입
    form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

def login(request):             # 로그인
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.user.is_authenticated:
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
        ):
            return redirect(next_url)
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
            ):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "registration/login.html",
        {"form": form, "next": next_url},
    )
