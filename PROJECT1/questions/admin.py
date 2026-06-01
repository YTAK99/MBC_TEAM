from django.contrib import admin

from .models import Question, QuestionAgree, Response, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_anonymous", "status", "created_at")
    list_filter = ("is_anonymous", "status", "tags")
    search_fields = ("title", "content")
    filter_horizontal = ("tags",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "response_type", "created_at")
    list_filter = ("response_type",)


@admin.register(QuestionAgree)
class QuestionAgreeAdmin(admin.ModelAdmin):
    list_display = ("question", "user", "created_at")

