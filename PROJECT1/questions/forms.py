from django import forms

# Django 기본 회원가입 폼
from django.contrib.auth.forms import UserCreationForm

# Django 기본 사용자 모델
from django.contrib.auth.models import User

# 정규표현식 사용
import re


# =========================
# 질문 작성 폼
# =========================
class QuestionForm(forms.Form):

    # 질문 제목 입력칸
    title = forms.CharField(

        # 화면에 표시할 이름
        label="제목",

        # 최대 글자 수
        max_length=100,

        # 입력칸 디자인 설정
        widget=forms.TextInput(
            attrs={

                # CSS 클래스
                "class": "input-field",

                # 입력 전 안내 문구
                "placeholder": "질문 제목을 입력하세요",
            }
        ),
    )

    # 질문 내용 입력칸
    content = forms.CharField(

        # 화면에 표시할 이름
        label="내용",

        # 여러 줄 입력창 사용
        widget=forms.Textarea(
            attrs={

                # CSS 클래스
                "class": "input-field form-textarea",

                # 입력 전 안내 문구
                "placeholder": "질문 내용을 입력하세요",

                # 입력창 높이
                "rows": 6,
            }
        ),
    )


# =========================
# 회원가입 폼
# =========================
class SignupForm(UserCreationForm):

    # 역할 선택 목록
    ROLE_CHOICES = [

        # 학생
        ("student", "학생"),

        # 강사
        ("teacher", "강사"),
    ]

    # 아이디 입력칸
    username = forms.CharField(

        # 화면에 표시할 이름
        label="아이디",

        # 입력칸 디자인 설정
        widget=forms.TextInput(
            attrs={

                # CSS 클래스
                "class": "input-field",

                # 입력 안내 문구
                "placeholder": "아이디 입력",
            }
        ),
    )

    # 비밀번호 입력칸
    password1 = forms.CharField(

        # 화면에 표시할 이름
        label="비밀번호",

        # 비밀번호 입력창 사용
        widget=forms.PasswordInput(
            attrs={

                # CSS 클래스
                "class": "input-field",

                # 입력 안내 문구
                "placeholder": "비밀번호 입력",
            }
        ),

        # 비밀번호 조건 안내
        help_text="영문 대소문자, 숫자를 포함한 8자 이상",
    )

    # 비밀번호 확인 입력칸
    password2 = forms.CharField(

        # 화면에 표시할 이름
        label="비밀번호 확인",

        # 비밀번호 입력창 사용
        widget=forms.PasswordInput(
            attrs={

                # CSS 클래스
                "class": "input-field",

                # 입력 안내 문구
                "placeholder": "비밀번호 확인",
            }
        ),
    )

    # 역할 선택 입력칸
    role = forms.ChoiceField(

        # 화면에 표시할 이름
        label="역할",

        # 선택 목록 사용
        choices=ROLE_CHOICES,

        # 라디오 버튼 형태로 출력
        widget=forms.RadioSelect,
    )

    class Meta:

        # Django User 모델 사용
        model = User

        # 회원가입에 사용할 필드
        fields = (
            "username",
            "password1",
            "password2",
        )

    # 비밀번호 검사 함수
    def clean_password1(self):

        # 입력된 비밀번호 가져오기
        password = self.cleaned_data.get("password1")

        # 비어있으면 그대로 반환
        if not password:
            return password

        # 8자 미만 검사
        if len(password) < 8:
            raise forms.ValidationError(
                "비밀번호는 8자 이상이어야 합니다."
            )

        # 대문자 포함 여부 검사
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "대문자를 포함해야 합니다."
            )

        # 소문자 포함 여부 검사
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "소문자를 포함해야 합니다."
            )

        # 숫자 포함 여부 검사
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError(
                "숫자를 포함해야 합니다."
            )

        # 조건 통과 시 비밀번호 반환
        return password

