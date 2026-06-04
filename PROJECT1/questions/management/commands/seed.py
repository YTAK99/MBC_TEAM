from random import choice, randint, sample

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Faker

from questions.models import (
    Profile,
    Question,
    QuestionAgree,
    Response,
    Tag,
)

fake = Faker("ko_KR")


class Command(BaseCommand):
    help = "시연용 데이터 생성"

    def handle(self, *args, **kwargs):

        self.stdout.write("시연 데이터 생성 시작...")

        # =========================
        # 태그 생성
        # =========================
        tag_data = [
            ("Python", "#3B82F6"),
            ("알고리즘", "#8B5CF6"),
            ("Django", "#10B981"),
            ("데이터베이스", "#F59E0B"),
            ("Git", "#EF4444"),
            ("개념", "#6B7280"),
        ]

        tags = []

        for name, color in tag_data:
            tag, _ = Tag.objects.get_or_create(
                name=name,
                defaults={"color": color},
            )
            tags.append(tag)

        # =========================
        # 학생 생성
        # =========================
        students = []

        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f"student{i}"
            )

            if created:
                user.set_password("1234")
                user.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={"role": "student"}
            )

            students.append(user)

        # =========================
        # 강사 생성
        # =========================
        teachers = []

        for i in range(1, 3):
            user, created = User.objects.get_or_create(
                username=f"teacher{i}"
            )

            if created:
                user.set_password("1234")
                user.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={"role": "teacher"}
            )

            teachers.append(user)

        # =========================
        # 질문 생성
        # =========================

        sample_titles = [
            "Django 로그인 오류 질문",
            "Git merge 충돌 해결 방법",
            "Python 리스트 정렬 질문",
            "ORM 사용 시 성능 문제",
            "ForeignKey와 ManyToMany 차이",
            "SQLite와 MySQL 차이점",
            "VSCode 디버깅 방법",
            "템플릿 상속이 안됩니다",
            "회원가입 구현 질문",
            "Bootstrap 적용 문제",
        ]

        statuses = [
            Question.Status.OPEN,
            Question.Status.ANSWERED,
            Question.Status.FOLLOW_UP,
            Question.Status.RESOLVED,
        ]

        questions = []

        for i in range(30):

            question = Question.objects.create(
                author=choice(students),
                title=choice(sample_titles),
                content=fake.text(max_nb_chars=300),
                status=choice(statuses),
                is_anonymous=choice([True, False]),
            )

            # 태그 1~3개 랜덤 부여
            selected_tags = sample(tags, randint(1, 3))
            question.tags.set(selected_tags)

            questions.append(question)

        # =========================
        # 답변 생성
        # =========================

        answer_contents = [
            "settings.py 설정을 확인해보세요.",
            "ForeignKey 관계를 다시 확인해보세요.",
            "마이그레이션을 다시 수행해보세요.",
            "Django 공식 문서를 참고하세요.",
            "select_related를 사용하는 것이 좋습니다.",
            "prefetch_related를 활용해보세요.",
            "템플릿 경로 설정을 확인하세요.",
            "urls.py를 다시 점검해보세요.",
        ]

        responses = []

        for i in range(50):

            question = choice(questions)

            # 강사 80%, 학생 20%
            author = (
                choice(teachers)
                if randint(1, 100) <= 80
                else choice(students)
            )

            response = Response.objects.create(
                question=question,
                author=author,
                response_type=Response.ResponseType.ANSWER,
                content=choice(answer_contents),
            )

            responses.append(response)

        # =========================
        # 채택 답변 생성
        # =========================

        resolved_questions = Question.objects.filter(
            status=Question.Status.RESOLVED
        )

        for question in resolved_questions:

            teacher_responses = question.responses.exclude(
                author=question.author
            )

            if teacher_responses.exists():

                accepted = teacher_responses.first()

                accepted.is_accepted = True
                accepted.save()

        # =========================
        # 공감 생성
        # =========================

        for question in questions:

            agree_users = sample(
                students,
                randint(0, len(students))
            )

            for user in agree_users:

                if user != question.author:

                    QuestionAgree.objects.get_or_create(
                        question=question,
                        user=user,
                    )

        # =========================
        # 결과 출력
        # =========================

        self.stdout.write(
            self.style.SUCCESS(
                f"""
==================================
시연 데이터 생성 완료

학생 : {len(students)}명
강사 : {len(teachers)}명
질문 : {Question.objects.count()}개
답변 : {Response.objects.count()}개
공감 : {QuestionAgree.objects.count()}개
==================================
"""
            )
        )