"""Формы приложения blog."""

from django import forms

from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма создания и редактирования блоговой записи."""

    class Meta:
        model = BlogPost
        fields = ("title", "content", "preview", "is_published")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Заголовок"},
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Содержимое",
                    "rows": 8,
                },
            ),
            "preview": forms.ClearableFileInput(
                attrs={"class": "form-control"},
            ),
            "is_published": forms.CheckboxInput(
                attrs={"class": "form-check-input"},
            ),
        }
