from django import template

register = template.Library()


def _profile_role(user):
    """
    회원가입·로그인·강사 페이지와 같은 역할 기준: Profile.role.
    Django User.is_staff(관리자 사이트 권한)와는 별개이다.
    """
    if hasattr(user, "profile"):
        return user.profile.role
    return "student"


@register.filter
def user_is_teacher(user):
    """Profile.role == 'teacher' 이면 True (회원가입 시 '강사' 선택과 동일)."""
    return _profile_role(user) == "teacher"


@register.filter
def user_role_label(user):
    """답변 배지 등에 쓸 표시 문자열: 강사 / 학생."""
    return "강사" if _profile_role(user) == "teacher" else "학생"
