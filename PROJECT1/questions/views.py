from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView
from django.contrib import messages

from .forms import QuestionForm, ResponseForm, SignupForm
from .models import (
    Question,
    QuestionAgree,
    Response,
    Tag,
    Profile,
)

def custom_404(request, exception):
    return render(request, "404.html", status=404)


def _redirect_by_role(user):
    # 역할에 따라 로그인 후 첫 화면을 분기한다.
    if hasattr(user, "profile") and user.profile.role == "teacher":
        return redirect("questions:teacher_home")
    return redirect("questions:home")

def _login_redirect(request):
    """로그인 후 원래 페이지로 돌아가도록 next 에 현재 URL 을 담아 리다이렉트."""
    return redirect_to_login(request.get_full_path())


def _board_query_params(*, sort="", query="", status_filter="", selected_tag_ids=None, mine=False):
    params = []
    if sort:
        params.append(("sort", sort))
    if status_filter:
        params.append(("status", status_filter))
    if query:
        params.append(("q", query))
    if mine:
        params.append(("mine", "1"))
    for tag_id in selected_tag_ids or []:
        params.append(("tag", tag_id))
    return params


def home(request):
    sort = request.GET.get("sort", "latest")
    current_status = request.GET.get("status", "")
#     questions = (
#         Question.objects
#         .prefetch_related("tags")
#         .annotate(agree_count=Count("agrees"))
#     )

#     if current_status == "NEW":
#         questions = questions.filter(status="OPEN")
#     elif current_status == "WAITING":
#         questions = questions.filter(status__in=["OPEN", "FOLLOW_UP", "ANSWERED"])
#     elif current_status in ["OPEN", "FOLLOW_UP", "ANSWERED", "RESOLVED"]:
#         questions = questions.filter(status=current_status)

#     if sort == "popular":
#         questions = questions.order_by("-agree_count", "-created_at")
#     else:
#         questions = questions.order_by("-created_at")

#     questions = questions[:5]
    
    return render(request, "questions/home.html", {
        "questions": [],
        "total_question_count": Question.objects.count(),
        "new_count": Question.objects.filter(
        status="OPEN"
        ).count(),

        "waiting_count": Question.objects.filter(
        status__in=["OPEN", "ANSWERED", "FOLLOW_UP"]
        ).count(),

        "resolved_count": Question.objects.filter(
        status="RESOLVED"
        ).count(),
        "current_sort": sort,
        "current_status": current_status,
})


def hall_of_fame(request):
    # 해결왕 순위 계산
    top_solvers = (
        User.objects
        .annotate(
            accepted_count=Count(
                "responses",
                filter=Q(responses__is_accepted=True),
            )
        )
        .filter(accepted_count__gt=0)
        .order_by("-accepted_count", "username")[:3]
    )
    # 답변왕은 답변 수로만 집계 (채택 여부는 상관 없음)
    top_responders = (
        User.objects
        .annotate(response_count=Count("responses"))
        .filter(response_count__gt=0)
        .order_by("-response_count", "username")[:3]
    )

    context = {
        "top_solvers": top_solvers,
        "top_responders": top_responders,
    }

    return render(request, "questions/hall_of_fame.html", context)


def board(request):
    sort = request.GET.get("sort", "latest")
    selected_tag_ids = request.GET.getlist("tag")
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    current_status = status_filter
    mine_requested = request.GET.get("mine") == "1"

    if mine_requested and not request.user.is_authenticated:
        return _login_redirect(request)

    questions = (
        Question.objects
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees"))
    )

    if mine_requested:
        questions = questions.filter(author=request.user)

    if status_filter == "NEW":
        questions = questions.filter(status="OPEN")

    elif status_filter == "WAITING":
        questions = questions.filter(
        status__in=["OPEN", "FOLLOW_UP", "ANSWERED"]
    )

    elif status_filter in ["OPEN", "FOLLOW_UP", "ANSWERED", "RESOLVED"]:
        questions = questions.filter(status=status_filter)

    elif status_filter == "RESOLVED":
        questions = questions.filter(status="RESOLVED")

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

        params = _board_query_params(
            sort=sort,
            query=query,
            status_filter=status_filter,
            selected_tag_ids=next_tag_ids,
            mine=mine_requested,
        )

        tag_filters.append({
            "tag": tag,
            "is_selected": tag_id in selected_tag_ids,
            "url": "?" + urlencode(params),
        })

    paginator = Paginator(questions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    mine_filter_url = "?" + urlencode(
        _board_query_params(
            sort=sort,
            query=query,
            status_filter=status_filter,
            selected_tag_ids=selected_tag_ids,
            mine=not mine_requested,
        )
    )

    return render(request, "questions/board.html", {
        "questions": page_obj,
        "page_obj": page_obj,
        "tags": tags,
        "tag_filters": tag_filters,
        "selected_tag_ids": selected_tag_ids,
        "current_sort": sort,
        "current_status": current_status,
        "query": query,
        "mine_active": mine_requested,
        "mine_filter_url": mine_filter_url,
    })


class AskView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = "questions/ask.html"
    login_url = "questions:login"

    def dispatch(self, request, *args, **kwargs):
        # 로그인 안 되어 있으면 메시지 표시 후 로그인 페이지 이동
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "로그인 후 질문할 수 있습니다."
            )
            return redirect("questions:login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["all_tags"] = Tag.objects.all()
        # 검증 실패로 폼을 다시 보여줄 때 사용자가 방금 고른 태그를 유지한다.
        if self.request.method == "POST":
            ctx["selected_tag_ids"] = [
                int(tag_id)
                for tag_id in self.request.POST.getlist("tags")
                if tag_id.isdigit()
            ]
        else:
            ctx["selected_tag_ids"] = []
        return ctx

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        form.save_m2m()
        return redirect("questions:detail", pk=question.pk)


def detail(request, pk):
    """
    질문 상세 페이지.
    - GET: 질문·답변 목록·답변 폼 표시
    - POST: 같은 URL 에서 Response 저장 (PRG 패턴으로 redirect)
    """
    question = get_object_or_404(
        Question.objects.select_related("author")
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees", distinct=True)),
        pk=pk,
    )

    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return _login_redirect(request)

        if question.is_resolved:
            return redirect("questions:detail", pk=pk)

        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.question = question
            response.author = request.user
            if request.user.id == question.author_id:
                response.response_type = Response.ResponseType.FOLLOW_UP
                question.status = Question.Status.FOLLOW_UP
            elif (
                hasattr(request.user, "profile")
                and request.user.profile.role == "teacher"
            ):
                response.response_type = Response.ResponseType.ANSWER
                question.status = Question.Status.ANSWERED
            else:  # 사용자가 학생인 경우
                response.response_type = Response.ResponseType.ANSWER
                question.status = Question.Status.ANSWERED
            response.save()
            question.save(update_fields=["status"])
            return redirect("questions:detail", pk=pk)
    else:
        form = ResponseForm()

        if request.user.is_authenticated and request.user.id == question.author_id:
            form.fields["content"].widget.attrs["placeholder"] = (
                "추가로 궁금한 내용을 입력해주세요..."
            )
        else:
            form.fields["content"].widget.attrs["placeholder"] = (
                "답변을 입력해주세요..."
            )

    # 답변 작성자 배지도 Profile.role 기준이므로 profile 까지 함께 조회
    responses = question.responses.select_related("author", "author__profile").all()

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


def resolve(request, pk):
    """질문 작성자 본인만 상태를 RESOLVED 로 변경할 수 있다."""
    if request.method != "POST":
        return redirect("questions:detail", pk=pk)

    question = get_object_or_404(Question, pk=pk)
    if not request.user.is_authenticated:
        return _login_redirect(request)

    if question.author_id == request.user.id:
        question.status = Question.Status.RESOLVED
        question.save(update_fields=["status"])

    return redirect("questions:detail", pk=pk)

@login_required
def accept_response(request, response_id):
    if request.method != "POST":
        return redirect("questions:home")

    response = get_object_or_404(Response, pk=response_id)
    question = response.question

    if request.user.id != question.author_id:
        return redirect("questions:detail", pk=question.pk)

    if response.author_id == question.author_id:
        return redirect("questions:detail", pk=question.pk)

    question.responses.update(is_accepted=False)

    response.is_accepted = True
    response.save(update_fields=["is_accepted"])

    question.status = Question.Status.RESOLVED
    question.save(update_fields=["status"])

    return redirect("questions:detail", pk=question.pk)

def agree_toggle(request, pk):
    """로그인 사용자의 '도움돼요' 공감 토글."""
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

# 질문 수정 기능 추가
@login_required
def edit(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.author_id != request.user.id:
        return redirect("questions:detail", pk=pk)

    if question.is_resolved:
        return redirect("questions:detail", pk=pk)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        # 수정 저장 실패 시에도 사용자가 선택한 태그 상태를 그대로 복원한다.
        selected_tag_ids = [
            int(tag_id)
            for tag_id in request.POST.getlist("tags")
            if tag_id.isdigit()
        ]
        if form.is_valid():
            form.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm(instance=question)
        # 수정 페이지 첫 진입 시 기존 질문에 연결된 태그를 미리 선택 상태로 전달한다.
        selected_tag_ids = list(
            question.tags.values_list("id", flat=True)
        )

    return render(request, "questions/ask.html", {
        "form": form,
        "all_tags": Tag.objects.all(),
        "selected_tag_ids": selected_tag_ids,
        "is_edit": True,
        "question": question,
    })
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            # 중복 프로필 생성을 막기 위해 get_or_create를 사용한다.
            # (관리자/스크립트 등으로 Profile이 이미 생긴 경우 대비)
            Profile.objects.get_or_create(
                user=user,
                defaults={"role": form.cleaned_data["role"]},
            )

            auth_login(
                request,
                user,
                # auth backend가 2개라 backend를 명시해야 ValueError를 피할 수 있다.
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return _redirect_by_role(user)

    else:
        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect("questions:home")


def check_username(request):
    username = request.GET.get("username", "").strip()
    exists = User.objects.filter(username=username).exists() if username else False
    return JsonResponse({"exists": exists})

def login(request):
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.user.is_authenticated:
        # 일반 로그인/구글 로그인을 포함해, 로그인된 사용자는
        # Profile 유무로 "역할 선택 완료" 상태를 판단한다.
        if not hasattr(request.user, "profile"):
            return redirect("questions:select_role")
        return _redirect_by_role(request.user)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            auth_login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
            ):
                return redirect(next_url)

            if (
                hasattr(user, "profile")
                and user.profile.role == "teacher"
            ):
                return redirect("questions:teacher_home")

            return redirect("questions:home")

    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "registration/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )


@login_required
def select_role(request):
    # 첫 로그인(프로필 미생성) 사용자만 역할 선택을 수행한다.
    if hasattr(request.user, "profile"):
        return _redirect_by_role(request.user)

    error = ""
    if request.method == "POST":
        selected_role = request.POST.get("role")
        if selected_role not in {"student", "teacher"}:
            error = "역할을 선택해주세요."
        else:
            # 동시 요청 등 예외 상황에서도 중복 생성되지 않게 보호한다.
            Profile.objects.get_or_create(
                user=request.user,
                defaults={"role": selected_role},
            )
            return _redirect_by_role(request.user)

    return render(request, "registration/select_role.html", {"error": error})

def is_teacher(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "teacher"
    )

@login_required
@user_passes_test(is_teacher)
def teacher_home(request):

    sort = request.GET.get("sort", "latest")
    current_status = request.GET.get("status", "")

    waiting_questions = (
        Question.objects
        .annotate(agree_count=Count("agrees"))
        .prefetch_related("tags")
    )

    if current_status in ["OPEN", "FOLLOW_UP", "ANSWERED", "RESOLVED"]:
        waiting_questions = waiting_questions.filter(status=current_status)
    else:
        waiting_questions = waiting_questions.filter(status__in=["OPEN", "FOLLOW_UP"])

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
        "current_status": current_status,
    }

    return render(request, "questions/teacher_home.html", context)



