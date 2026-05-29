from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import re

from .models import Question, Response


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content", "is_anonymous"]
        labels = {
            "title": "제목",
            "content": "내용",
            "is_anonymous": "익명으로 작성하기",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input-field",
                    "placeholder": "질문 제목을 입력하세요",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "input-field form-textarea",
                    "placeholder": "질문 내용을 입력하세요",
                    "rows": 6,
                }
            ),
        }


class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ("student", "학생"),
        ("teacher", "강사"),
    ]

    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                "class": "input-field",
                "placeholder": "아이디 입력",
            }
        ),
    )

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "비밀번호 입력",
            }
        ),
        help_text="영문 대소문자, 숫자를 포함한 8자 이상",
    )

    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "비밀번호 확인",
            }
        ),
    )

    role = forms.ChoiceField(
        label="역할",
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not password:
            return password
        if len(password) < 8:
            raise forms.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("대문자를 포함해야 합니다.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("소문자를 포함해야 합니다.")
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("숫자를 포함해야 합니다.")
        return password


class ResponseForm(forms.ModelForm):
    """
    질문 상세 페이지 하단 '답변 남기기' 폼.
    question/author/response_type 은 views.detail POST 처리에서 저장한다.
    """

    class Meta:
        model = Response
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "input-field form-textarea",
                    "rows": 3,
                    "placeholder": "답변을 입력해주세요...",
                }
            )
        }
