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
from .models import Question, QuestionAgree, Response, Tag


def _login_redirect(request):
    """로그인 후 원래 페이지로 돌아가도록 next 에 현재 URL 을 담아 리다이렉트."""
    return redirect_to_login(request.get_full_path())


def home(request):
    sort = request.GET.get("sort", "latest")
    current_status = request.GET.get("status", "")
    questions = (
        Question.objects
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees"))
    )

    if current_status == "NEW":
        questions = questions.filter(status="OPEN")
    elif current_status == "WAITING":
        questions = questions.filter(status__in=["OPEN", "FOLLOW_UP", "ANSWERED"])
    elif current_status in ["OPEN", "FOLLOW_UP", "ANSWERED", "RESOLVED"]:
        questions = questions.filter(status=current_status)

    if sort == "popular":
        questions = questions.order_by("-agree_count", "-created_at")
    else:
        questions = questions.order_by("-created_at")

    questions = questions[:5]
    
    return render(request, "questions/home.html", {
        "questions": questions,
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
    """
    명예의 전당 — 추후 구현 예정.

    top_questioners: 질문을 많이 작성한 사용자 순위
      예) [{"user": user, "count": 12}, ...]
    top_responders: 답변을 많이 작성한 사용자 순위
      예) [{"user": user, "count": 8}, ...]
    """
    # TODO: Question·Response 를 author 기준으로 집계해 순위 데이터를 채운다.
    context = {
        "top_questioners": [],
        "top_responders": [],
    }
    return render(request, "questions/hall_of_fame.html", context)


def board(request):
    sort = request.GET.get("sort", "latest")
    selected_tag_ids = request.GET.getlist("tag")
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    current_status = status_filter

    questions = (
        Question.objects
        .prefetch_related("tags")
        .annotate(agree_count=Count("agrees"))
    )

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
        "current_status": current_status,
        "query": query,
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
            if request.user.is_staff:
                response.response_type = Response.ResponseType.ANSWER
                question.status = Question.Status.ANSWERED
            else:
                response.response_type = Response.ResponseType.FOLLOW_UP
                question.status = Question.Status.FOLLOW_UP
            response.save()
            question.save(update_fields=["status"])
            return redirect("questions:detail", pk=pk)
    else:
        form = ResponseForm()

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
        if form.is_valid():
            form.save()
            return redirect("questions:detail", pk=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, "questions/ask.html", {
        "form": form,
        "all_tags": Tag.objects.all(),
        "is_edit": True,
        "question": question,
    })

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("questions:home")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})


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


def is_teacher(user):
    return user.is_authenticated and user.is_staff


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


@login_required
@user_passes_test(is_teacher)
def teacher_question_list(request):
    sort = request.GET.get("sort", "latest")
    selected_tag_ids = request.GET.getlist("tag")
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    current_status = status_filter

    questions = (
        Question.objects
        .annotate(agree_count=Count("agrees"))
        .prefetch_related("tags")
    )

    if status_filter in [
        "OPEN",
        "FOLLOW_UP",
        "ANSWERED",
        "RESOLVED"
    ]:
        questions = questions.filter(status=status_filter)
    else:
        questions = questions.filter(status__in=["OPEN", "FOLLOW_UP"])

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
        if status_filter:
            params.append(("status", status_filter))
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

    context = {
        "questions": page_obj,
        "page_obj": page_obj,
        "tags": tags,
        "tag_filters": tag_filters,
        "selected_tag_ids": selected_tag_ids,
        "current_sort": sort,
        "current_status": current_status,
        "query": query,
    }

    return render(request, "questions/teacher_board.html", context)
