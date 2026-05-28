from django.shortcuts import render, redirect
from django.contrib.auth import logout, login

from .forms import QuestionForm, SignupForm


def home(request):
    return render(request, "questions/home.html")


def board(request):
    return render(request, "questions/board.html")


def ask(request):
    form = QuestionForm()
    return render(request, "questions/ask.html", {"form": form})


def detail(request, pk):
    return render(request, "questions/detail.html", {"question_id": pk})


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            # 회원가입 후 자동 로그인
            login(request, user)

            return redirect("/")

    else:
        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form},
    )


def logout_view(request):
    logout(request)
    return redirect('/')