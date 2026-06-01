from django.conf import settings
from django.db import models

#카테고리 스티커
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):   # 질문 등록 신청서 양식
    class Status(models.TextChoices):
        OPEN = "OPEN", "답변 대기"
        ANSWERED = "ANSWERED", "답변 완료"
        FOLLOW_UP = "FOLLOW_UP", "추가 질문"
        RESOLVED = "RESOLVED", "해결됨"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # 누구랑 연결할건지?
        on_delete=models.CASCADE,   # 회원탈퇴 시 이 글을 어떡하나?
        related_name="questions",   # 반대로 부를 땐 뭐라고 할까?
    )
    #빈칸들(필드):제목, 내용, 익명체크란 등 작성자가 채워 놓을 공간들 
    title = models.CharField(max_length=100)    # 캐릭터필드; 한 줄짜리 짧은 글(이름, 제목 주소 등)을 입력받는 상자.
    content = models.TextField()    # 텍스트필드; 블로그 본문이나 질문 내용처럼 여러 줄의 긴 글을 입력받는 상자 
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)   # choices=Status.choices ;status의 규칙 안에 선택지들 안에서 골라라
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)    # 다대다필드; 태그가 하나/여러개 가능
    
    is_anonymous = models.BooleanField(default=False)   #불리언필드; True/False 상태확인 
    # BooleanField는 True.False의 값을 저정하는 필드 . '익명으로 올리기' 토클이 켜지면 True, 꺼지면 False저장. 

    created_at = models.DateTimeField(auto_now_add=True)    # created_at; 작성시간 칸 (날짜+시간). 
    updated_at = models.DateTimeField(auto_now=True)    # updated_at; 수정시간 칸 (날짜+시간)-> 수정하여 저장시 현재시간으로 업데이트  

    class Meta: # 게시판 글들을 항상 최신순으로 정렬 
        ordering = ["-created_at"]

    def __str__(self):  #글을 쓰면 번호(1, 2..)가 아닌 글제목으로
        return self.title

    @property
    def is_resolved(self):
        """
        템플릿에서 상태 비교 코드를 매번 쓰지 않도록
        '해결됨' 여부를 불리언 값으로 제공한다.
        """
        return self.status == self.Status.RESOLVED
    # def agree_count(self):
    #     return self.agrees.count()
    
    # 화면에 이름 대신 '익명'으로 바꿔서 보여주는 기능
    def display_author(self):
        if self.is_anonymous == True:   # 이 질문 양식(self)의(.) 익명 체크칸(is_anonymous)에 들어가는 값이 true면 
            return "익명"
        else:
            return self.author.username  # 이 질문양식(self)의(.) 작성자(author)의(.) 이름(username)을 리턴  

#질문을 읽고 달아주는 "답변양식"
class Response(models.Model):
    class ResponseType(models.TextChoices):
        ANSWER = "ANSWER", "강사/조교 답변"
        FOLLOW_UP = "FOLLOW_UP", "학생 추가 질문"

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    response_type = models.CharField(max_length=20, choices=ResponseType.choices)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.question.title} - {self.response_type}"

#다른 학생이 질문을 보고 공감/좋아요 버튼
class QuestionAgree(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="agrees",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="question_agrees",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"],
                name="unique_question_agree",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.question}"
