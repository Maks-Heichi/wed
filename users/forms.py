"""Формы приложения users."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя по электронной почте."""

    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.ru",
            }
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Повторите пароль",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        """Проверяет уникальность электронной почты."""
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован.")
        return email


class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя по электронной почте и паролю."""

    username = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.ru",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Неверная электронная почта или пароль.",
        "inactive": "Учётная запись деактивирована.",
    }

    def clean_username(self):
        """Приводит email к нижнему регистру для корректной авторизации."""
        return self.cleaned_data.get("username", "").strip().lower()
