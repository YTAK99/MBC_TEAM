from django.db.models import Count
from django.shortcuts import render

from .forms import QuestionForm, SignupForm
from .models import Question, Tag

def home(request):              # 홈 페이지
    return render(request, "questions/home.html")


def board(request):             # 질문 목록 페이지
    sort = request.GET.get("sort", "latest")
    tag_id = request.GET.get("tag")
    query = request.GET.get("q", "")

    questions = (
        Question.objects
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees"))
    )
    
    if query:
        questions = questions.filter(title__icontains=query)

    if tag_id:
        questions = questions.filter(tags__id=tag_id)

    if sort == "popular":
        questions = questions.order_by("-agree_count", "-created_at")
    else:
        questions = questions.order_by("-created_at")
    
    tags = Tag.objects.all()
            
    return render(request, "questions/board.html", {
        "questions": questions,
        "tags": tags,
        "selected_tag_id": tag_id,
        "sort": sort,
        "query": query,
    })


def ask(request):               # 질문/추가답변 생성 페이지
    form = QuestionForm()
    return render(request, "questions/ask.html", {"form": form})


def detail(request, pk):        # 질문 상세 페이지
    return render(request, "questions/detail.html", {"question_id": pk})


def signup(request):            # 회원가입
    form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

def login(request):             # 로그인
    return render(request, "registration/login.html")
