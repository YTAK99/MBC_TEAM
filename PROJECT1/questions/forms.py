from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    class Meta:
        model = User
        fields = ("username",)
    
# 답변 작성 폼
class ResponseForm(forms.ModelForm):

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
