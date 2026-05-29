from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import QuestionForm, SignupForm
from .models import Question


def home(request):

    questions = Question.objects.all()[:5]

    question_count = Question.objects.count()

    return render(
        request,
        "questions/home.html",
        {
            "questions": questions,
            "question_count": question_count,
        },
    )


def board(request):

    questions = Question.objects.all()

    return render(
        request,
        "questions/board.html",
        {
            "questions": questions,
        },
    )


@login_required
def ask(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            Question.objects.create(
                author=request.user,
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
            )

            return redirect("questions:board")

    else:
        form = QuestionForm()

    return render(
        request,
        "questions/ask.html",
        {
            "form": form,
        },
    )


def detail(request, pk):

    question = Question.objects.get(pk=pk)

    return render(
        request,
        "questions/detail.html",
        {
            "question": question,
        },
    )


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("questions:home")

    else:
        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
        },
    )


def logout_view(request):

    logout(request)

    return redirect("questions:home")


def check_username(request):

    username = request.GET.get("username")

    exists = User.objects.filter(
        username=username
    ).exists()

    return JsonResponse({
        "exists": exists
    })
