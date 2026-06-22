"""Контроллеры приложения users."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import UserLoginForm, UserRegisterForm


class RegisterView(FormView):
    """Регистрирует пользователя и отправляет приветственное письмо."""

    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        """Перенаправляет авторизованного пользователя на главную."""
        if request.user.is_authenticated:
            return self.redirect_authenticated_user()
        return super().dispatch(request, *args, **kwargs)

    def redirect_authenticated_user(self):
        """Возвращает редирект для уже авторизованного пользователя."""
        from django.shortcuts import redirect

        return redirect(self.get_success_url())

    def form_valid(self, form):
        """Создаёт пользователя, выполняет вход и отправляет письмо."""
        user = form.save()
        login(self.request, user)
        try:
            self.send_welcome_email(user.email)
            messages.success(self.request, "Регистрация прошла успешно. Проверьте почту.")
        except Exception:
            messages.warning(
                self.request,
                "Регистрация прошла успешно, но письмо не удалось отправить.",
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Показывает сообщение об ошибках валидации формы."""
        messages.error(self.request, "Исправьте ошибки в форме регистрации.")
        return super().form_invalid(form)

    def send_welcome_email(self, user_email: str) -> None:
        """Отправляет приветственное письмо на электронную почту пользователя."""
        subject = "Добро пожаловать в Skystore"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )


class UserLoginView(LoginView):
    """Авторизует пользователя по электронной почте и паролю."""

    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        """Показывает сообщение при неверных данных для входа."""
        messages.error(self.request, "Неверная электронная почта или пароль.")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Завершает сессию пользователя."""

    next_page = reverse_lazy("catalog:home")
