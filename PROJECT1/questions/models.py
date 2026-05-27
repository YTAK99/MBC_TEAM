from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "답변 대기"
        ANSWERED = "ANSWERED", "답변 완료"
        FOLLOW_UP = "FOLLOW_UP", "추가 질문"
        RESOLVED = "RESOLVED", "해결됨"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.question.title} - {self.response_type}"


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
