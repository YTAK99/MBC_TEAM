from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


from .forms import QuestionForm, SignupForm
from .models import Tag

def home(request):              # 홈 페이지
    return render(request, "questions/home.html")


def board(request):             # 질문 목록 페이지
    return render(request, "questions/board.html")

# 질문/추가답변 생성 페이지
class AskView(LoginRequiredMixin, CreateView): # LoginRequiredMixin, CreateView는 장고의 내장 부품(views.py에서만 등장)
# LoginRequiredMixin (로그인+필수적인+기능짜집기 부품) : 사용자가 로그인 상태인지 확인후 비회원이라면 로그인 페이지로 이동
#                                                   회원이라면 글쓰기 화면(CreateView)로 이동 
#()안에 있는 이유? 장고의 내장 부품을 이용해서 AskView를 만들기 위해 
    form_class = QuestionForm
    template_name = "questions/ask.html"    # 사용자에게 보여줄 디자인은 ask.html 파일 안에서 가져와 !
    login_url = "login" # 로그인 안된 사람이 글을 작성하려 할 때는 login으로 넘어가 !
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["all_tags"] = Tag.objects.all()    
        return ctx
    # ctx ; context의 축약어.views.py가 ask.html에게 데이터를 보낼때 사용하는 상자 같은 의미의 단어

# 등록 버튼을 누르면 글이 저장
    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        form.save_m2m()
        return redirect("questions:detail", pk=question.pk)

def detail(request, pk):        # 질문 상세 페이지
    return render(request, "questions/detail.html", {"question_id": pk})


def signup(request):            # 회원가입
    form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

def login(request):             # 로그인
    return render(request, "registration/login.html")
