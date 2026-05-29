from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class QuestionForm(forms.Form):

    title = forms.CharField(
        label="제목",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "input-field",
                "placeholder": "질문 제목을 입력하세요",
            }
        ),
    )

    content = forms.CharField(
        label="내용",
        widget=forms.Textarea(
            attrs={
                "class": "input-field form-textarea",
                "placeholder": "질문 내용을 입력하세요",
                "rows": 6,
            }
        ),
    )


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
        fields = (
            "username",
            "password1",
            "password2",
        )

    def clean_password1(self):

        password = self.cleaned_data.get("password1")

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError(
                "비밀번호는 8자 이상이어야 합니다."
            )

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "대문자를 포함해야 합니다."
            )

        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "소문자를 포함해야 합니다."
            )

        if not re.search(r"[0-9]", password):
            raise forms.ValidationError(
                "숫자를 포함해야 합니다."
            )

        return password