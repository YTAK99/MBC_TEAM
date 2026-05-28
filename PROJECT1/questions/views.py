from django.db.models import Count, Q
from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import QuestionForm, SignupForm
from .models import Question, Tag
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required, user_passes_test

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
    # 검색어가 있는 경우 제목과 내용에서 검색어가 포함된 질문을 필터링
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
            next_tag_ids.remove(tag_id)     # 현재 태그가 선택된 상태라면, 클릭 시 선택 해제되도록 다음 태그 ID 목록에서 제거
        else:
            next_tag_ids.append(tag_id)

        params = []                     # URL에 현재 정렬 방식과 검색어, 선택된 태그들을 유지하기 위한 파라미터 목록

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
    # 페이지네이션
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

# 강사 구별용 함수
def is_teacher(user):
    return user.is_authenticated and user.is_staff

@login_required                 # 로그인한 사용자만 접근 가능하도록 데코레이터 추가
@user_passes_test(is_teacher)   # 강사만 접근 가능
# 강사용 홈 페이지 뷰 함수
def teacher_home(request):
    sort = request.GET.get("sort", "latest")

    waiting_questions = (
        Question.objects
        .filter(status__in=["OPEN", "FOLLOW_UP"])
        .annotate(agree_count=Count("agrees"))
        .prefetch_related("tags")
    )

    if sort == "popular":
        waiting_questions = waiting_questions.order_by("-agree_count", "-created_at")
    else:
        waiting_questions = waiting_questions.order_by("-created_at")

    waiting_questions = waiting_questions[:5]

    context = {
        "waiting_questions": waiting_questions,
        "open_count": Question.objects.filter(status="OPEN").count(),
        "follow_up_count": Question.objects.filter(status="FOLLOW_UP").count(),
        "answered_count": Question.objects.filter(status="ANSWERED").count(),
        "current_sort": sort,
    }

    return render(request, "questions/teacher_home.html", context)

@login_required
@user_passes_test(is_teacher)
# 강사용 질문 목록 페이지 뷰 함수
def teacher_question_list(request):
    sort = request.GET.get("sort", "latest")
    selected_tag_ids = request.GET.getlist("tag")
    query = request.GET.get("q", "")
    
    questions = (
        Question.objects
        .filter(status__in=["OPEN", "FOLLOW_UP"]) # 강사용 페이지에서는 OPEN과 FOLLOW_UP 상태의 질문만 보여줌
        .annotate(agree_count=Count("agrees"))
        .prefetch_related("tags")
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
            next_tag_ids.remove(tag_id)     # 현재 태그가 선택된 상태라면, 클릭 시 선택 해제되도록 다음 태그 ID 목록에서 제거
        else:
            next_tag_ids.append(tag_id)

        params = []                     # URL에 현재 정렬 방식과 검색어, 선택된 태그들을 유지하기 위한 파라미터 목록

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

    # 페이지네이션
    paginator = Paginator(questions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "questions": page_obj,
        "page_obj": page_obj,
        "tags": tags,
        "tag_filters": tag_filters,
        "selected_tag_ids": selected_tag_ids,
        "current_sort": sort,
        "query": query,
    }

    return render(request, "questions/teacher_board.html", context)