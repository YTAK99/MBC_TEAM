from winreg import QueryReflectionKey
from django import forms    # 장고 프로그램 패키지 안에서 화면 입력창을 담당하는 forms라는 도구 상자를 이 파일로 가져오겠음 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question    # models.py파일 안에서 Question 데이터 설계도를 끌고와라 

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question    #질문 작성 화면 양식은 models.py에서 가져온 class Question 기반으로 뼈대를 잡는것
        fields = ("title", "content", "tags", "is_anonymous")   #튜플형태/ class Question에 있는 것들 중 화면에서 나타나 입력받을 칸을 4개만 골라줌(나머지는 화면에 나타나지X)

        # 입력/버튼 상자들의 이름표 
        labels = {
            "title": "제목",
            "content": "내용",
            "tags": "태그 (최대 3개까지 가능합니다)",
            "is_anonymous": "익명으로 올리기",
        }
        # 입력 상자의 모양과 스타일 ;코드구조: "칸이름": 상자의 종류(옵션들)
        widgets = {                     # widgets={ labels안에 붙은 상자들의 html형태와 css등을 세부정의 }
            # 제목(title) 창 꾸미기
            "title": forms.TextInput(
                attrs={ #속성 
                    "placeholder": "제목은 간결하게 입력해주세요",  #placeholder;html에서 사용하는 용어. 입력창이 비어있을때 사용자에게 알려주는 임시 안내 텍스트
                    "class": "input-field",
                    "style": "width: 100%; background-color: #F5F3EE; border: none; border-radius: 12px; padding: 14px 16px; font-size: 14px; outline: none;",
                }
            ),
            #내용(content) 창 꾸미기
            "content": forms.Textarea(  # 여러줄을 쓸 수 있는 커다란 글상자 <textarea> 만들기
                attrs={
                    "placeholder": "어떤부분이 어려운지 구체적으로 설명해주세요",
                    "rows": 5,   # 글상자의 세로 높이는 5줄크기로 고정
                    "class": "input-field resize-none", # 사용자가 임의로 입력상자의 크기를 조정할수없게 고정 
                    "style": "width: 100%; background-color: #F5F3EE; border: none; border-radius: 12px; padding: 14px 16px; font-size: 14px; outline: none; resize: none;",
                }
            ),
            #태그(tags) 창 꾸미기
            "tags": forms.CheckboxSelectMultiple(), #여러개 선택가능한 태그들
            
            #익명으로 올리기 버튼(is_anonymous)
            "is_anonymous": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }



    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        if tags and tags.count() > 3:
            raise forms.ValidationError("태그는 최대 3개까지 선택할 수 있습니다.")
        return tags


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
