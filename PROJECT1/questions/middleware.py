from django.shortcuts import redirect
from django.urls import reverse


class RoleSelectionRequiredMiddleware:
    """
    로그인한 사용자 중 Profile(역할) 미완료 사용자는
    역할 선택 페이지로 유도한다.
    (구글 로그인처럼 allauth 경로로 들어온 경우도 동일하게 적용)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and not hasattr(user, "profile"):
            select_role_path = reverse("questions:select_role")
            allowed_prefixes = (
                select_role_path,
                reverse("questions:logout"),
                "/accounts/",  # allauth 소셜 콜백/로그아웃 경로
                "/admin/",     # 관리자 접근은 막지 않음
                "/static/",
            )
            if not request.path.startswith(allowed_prefixes):
                return redirect("questions:select_role")

        return self.get_response(request)
