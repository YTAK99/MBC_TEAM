from django.db.models import Count, Q
from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import QuestionForm, SignupForm
from .models import Question, Tag
from urllib.parse import urlencode

def home(request):              # 홈 페이지
    return render(request, "questions/home.html")


def board(request):             # 질문 목록 페이지
    sort = request.GET.get("sort", "latest")        
    selected_tag_ids = request.GET.getlist("tag")
    query = request.GET.get("q", "")

    questions = (                   # 질문 목록을 가져올 때 태그 정보와 공감 수를 함께 가져오기 위해 prefetch_related와 annotate 사용
        Question.objects
        .prefetch_related("tags")       # 질문과 관련된 태그 정보를 미리 가져와서 DB 쿼리 수를 줄임
        .annotate(agree_count=Count("agrees"))  # 각 질문에 대한 공감 수를 계산하여 agree_count 필드로 추가
    )
    
    if query:
        questions = questions.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
    )
    if selected_tag_ids:
        for tag_id in selected_tag_ids:
            questions = questions.filter(tags__id=tag_id)

    if sort == "popular":
        questions = questions.order_by("-agree_count", "-created_at")
    else:
        questions = questions.order_by("-created_at")

    tags = Tag.objects.all()

    tag_filters = []

    for tag in tags:
        tag_id = str(tag.id)
        next_tag_ids = selected_tag_ids.copy()

        if tag_id in next_tag_ids:
            next_tag_ids.remove(tag_id)
        else:
            next_tag_ids.append(tag_id)

        params = []

        if sort:
            params.append(("sort", sort))

        if query:
            params.append(("q", query))

        for selected_id in next_tag_ids:
            params.append(("tag", selected_id))

        tag_filters.append({
            "tag": tag,
            "is_selected": tag_id in selected_tag_ids,
            "url": "?" + urlencode(params),
        })

    paginator = Paginator(questions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "questions/board.html", {
        "questions": page_obj,
        "page_obj": page_obj,
        "tags": tags,
        "tag_filters": tag_filters,
        "selected_tag_ids": selected_tag_ids,
        "current_sort": sort,
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
