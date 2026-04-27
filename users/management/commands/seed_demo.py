"""
Тестовые данные для локальной проверки TeamFinder (вариант 3).

Запуск из корня проекта (с активированным venv и поднятой БД):

    python manage.py seed_demo

Повторный запуск дополняет только отсутствующие сущности (по email проекта / названию).

Очистить только демо-пользователей и их проекты:

    python manage.py seed_demo --clear

Свой пароль для всех демо-пользователей:

    python manage.py seed_demo --password mysecret
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project, Skill
from users.models import User

DEMO_EMAIL_DOMAIN = "@demo.teamfinder.local"


class Command(BaseCommand):
    help = "Создаёт демо-пользователей, навыки и проекты для теста."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="demo12345",
            help="Пароль для всех создаваемых демо-пользователей (по умолчанию demo12345).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help=f"Удалить пользователей с email *{DEMO_EMAIL_DOMAIN} и связанные проекты, затем заново засеять.",
        )

    def handle(self, *args, **options):
        password = options["password"]

        if options["clear"]:
            self._clear_demo()

        skill_names = [
            "Python",
            "Django",
            "PostgreSQL",
            "React",
            "Figma",
            "Docker",
            "JavaScript",
            "TypeScript",
            "REST API",
            "Git",
        ]
        skills = {}
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill

        users_spec = [
            {
                "email": f"alex{DEMO_EMAIL_DOMAIN}",
                "name": "Алексей",
                "surname": "Иванов",
                "phone": "+79001110001",
                "github_url": "https://github.com/demo-alex",
                "about": "Бэкенд и pet-проекты на Django.",
            },
            {
                "email": f"marina{DEMO_EMAIL_DOMAIN}",
                "name": "Марина",
                "surname": "Козлова",
                "phone": "+79001110002",
                "github_url": "https://github.com/demo-marina",
                "about": "UI/UX, дизайн интерфейсов.",
            },
            {
                "email": f"dmitry{DEMO_EMAIL_DOMAIN}",
                "name": "Дмитрий",
                "surname": "Соколов",
                "phone": "+79001110003",
                "github_url": "https://github.com/demo-dmitry",
                "about": "Fullstack, интересуют стартапы и open source.",
            },
            {
                "email": f"anna{DEMO_EMAIL_DOMAIN}",
                "name": "Анна",
                "surname": "Новикова",
                "phone": "+79001110004",
                "github_url": "",
                "about": "Тестирование и документация.",
            },
        ]

        with transaction.atomic():
            for spec in users_spec:
                existing = User.objects.filter(email=spec["email"]).first()
                if existing:
                    user = existing
                    self.stdout.write(f"Уже есть: {user.email}")
                    user.name = spec["name"]
                    user.surname = spec["surname"]
                    user.phone = spec["phone"]
                    user.github_url = spec["github_url"]
                    user.about = spec["about"]
                    user.save(
                        update_fields=[
                            "name",
                            "surname",
                            "phone",
                            "github_url",
                            "about",
                        ]
                    )
                    continue

                user = User.objects.create_user(
                    email=spec["email"],
                    password=password,
                    name=spec["name"],
                    surname=spec["surname"],
                )
                user.phone = spec["phone"]
                user.github_url = spec["github_url"]
                user.about = spec["about"]
                user.save(update_fields=["phone", "github_url", "about"])
                self.stdout.write(
                    self.style.SUCCESS(f"Создан пользователь: {user.email}")
                )

        alex = User.objects.get(email=f"alex{DEMO_EMAIL_DOMAIN}")
        marina = User.objects.get(email=f"marina{DEMO_EMAIL_DOMAIN}")
        dmitry = User.objects.get(email=f"dmitry{DEMO_EMAIL_DOMAIN}")
        anna = User.objects.get(email=f"anna{DEMO_EMAIL_DOMAIN}")

        projects_spec = [
            {
                "owner": alex,
                "name": "TeamFinder-клон: бэкенд",
                "description": "Pet-проект: платформа для поиска команды. API на Django, PostgreSQL.",
                "status": Project.STATUS_OPEN,
                "github_url": "https://github.com/demo/teamfinder-backend",
                "skill_names": ["Python", "Django", "PostgreSQL", "REST API", "Docker"],
                "participant_emails": [marina.email, dmitry.email],
            },
            {
                "owner": marina,
                "name": "Дизайн-система для стартапа",
                "description": "Компоненты в Figma, токены, гайд для разработчиков.",
                "status": Project.STATUS_OPEN,
                "github_url": "https://github.com/demo/design-system",
                "skill_names": ["Figma", "JavaScript", "React"],
                "participant_emails": [alex.email],
            },
            {
                "owner": dmitry,
                "name": "Мини-SaaS учёта задач",
                "description": "Закрытый цикл: идея взята из личного опыта. Ищем фронтендера.",
                "status": Project.STATUS_CLOSED,
                "github_url": "https://github.com/demo/task-saas",
                "skill_names": ["TypeScript", "React", "REST API", "Docker"],
                "participant_emails": [anna.email, alex.email],
            },
            {
                "owner": anna,
                "name": "Документация API на Read the Docs",
                "description": "Шаблоны OpenAPI и автогенерация примеров.",
                "status": Project.STATUS_OPEN,
                "github_url": "",
                "skill_names": ["Python", "Git"],
                "participant_emails": [dmitry.email],
            },
        ]

        with transaction.atomic():
            for p in projects_spec:
                project, created = Project.objects.get_or_create(
                    owner=p["owner"],
                    name=p["name"],
                    defaults={
                        "description": p["description"],
                        "status": p["status"],
                        "github_url": p["github_url"],
                    },
                )
                if not created:
                    project.description = p["description"]
                    project.status = p["status"]
                    project.github_url = p["github_url"]
                    project.save(
                        update_fields=["description", "status", "github_url"]
                    )
                    self.stdout.write(f"Обновлён проект: {project.name}")
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Создан проект: {project.name}")
                    )

                project.participants.add(p["owner"])
                for email in p["participant_emails"]:
                    u = User.objects.get(email=email)
                    project.participants.add(u)

                project.skills.set([skills[n] for n in p["skill_names"]])

        self.stdout.write(
            self.style.SUCCESS(
                "\nГотово. Войдите под любым демо-email и паролем из --password "
                f"(по умолчанию demo12345). Домен email: {DEMO_EMAIL_DOMAIN}"
            )
        )

    def _clear_demo(self):
        qs = User.objects.filter(email__endswith=DEMO_EMAIL_DOMAIN)
        count_u = qs.count()
        # проекты удалятся каскадно с owner; участники — M2M очистится
        qs.delete()
        self.stdout.write(
            self.style.WARNING(
                f"Удалено демо-пользователей: {count_u} (и их проекты каскадно)."
            )
        )
