from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm, SignupForm, ResponseForm
from .models import Question, QuestionAgree, Response

def home(request):              # 홈 페이지
    return render(request, "questions/home.html")


def board(request):             # 질문 목록 페이지
    return render(request, "questions/board.html")


def ask(request):               # 질문/추가답변 생성 페이지
    # 질문 작성은 로그인 사용자만 허용
    if not request.user.is_authenticated:
        return redirect("questions:login")

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


def detail(request, pk):        # 질문 상세 페이지
    # URL 로 전달받은 pk 로 질문 조회 (없으면 404)
    question = get_object_or_404(Question, pk=pk)

    # POST 요청이면 답변 작성 처리
    if request.method == "POST":
        # 로그인하지 않은 사용자는 답변 작성 불가
        if not request.user.is_authenticated:
            return redirect("questions:login")

        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.question = question          # 어떤 질문의 답변인지 연결
            response.author = request.user        # 작성자 연결
            # 현재 상세 페이지는 "질문 후속 글" 성격이므로 FOLLOW_UP 으로 저장
            response.response_type = Response.ResponseType.FOLLOW_UP
            response.save()
            return redirect("questions:detail", pk=pk)
    else:
        # GET 요청이면 빈 답변 폼 생성
        form = ResponseForm()

    # 질문에 달린 답변을 작성 순으로 조회해서 템플릿으로 전달
    responses = question.responses.select_related("author").all()
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
        return redirect("questions:login")

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
        return redirect("questions:login")

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
    return render(request, "registration/login.html")
