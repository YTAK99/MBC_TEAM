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
    class Meta:
        model = User
        fields = ("username",)
