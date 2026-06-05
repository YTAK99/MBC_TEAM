from django.shortcuts import render

# Create your views here.
def dashboard(request):     # 메인 대시보드 페이지
    return render(request, 'feedback/dashboard.html')       # dashboard.html 화면 출력

def signin(request):
    return render(request, 'feedback/pages/sign-in.html')