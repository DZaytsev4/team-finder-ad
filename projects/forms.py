from django import forms

from projects.validators import github_url_validator

from .models import Project

PROJECT_DESCRIPTION_ROWS = 6


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        labels = {
            "name": "Название проекта",
            "description": "Описание проекта",
            "github_url": "Ссылка на репозиторий GitHub",
            "status": "Статус проекта",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Название проекта",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": PROJECT_DESCRIPTION_ROWS,
                    "placeholder": "Описание проекта",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "placeholder": "https://github.com/логин/название-репозитория",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (Project.STATUS_OPEN, "Открыт"),
            (Project.STATUS_CLOSED, "Закрыт"),
        ]

    def clean_github_url(self):
        value = self.cleaned_data.get("github_url") or ""
        value = value.strip()
        if value:
            github_url_validator(value)
        return value
