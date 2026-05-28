from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "input-field",
                "placeholder": "이메일 입력",
            }
        ),
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input-field",
                "placeholder": "아이디 입력",
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "비밀번호 입력",
            }
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "비밀번호 확인",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )