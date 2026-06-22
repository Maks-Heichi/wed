from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователей с авторизацией по электронной почте."""

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт обычного пользователя."""
        if not email:
            raise ValueError("Email обязателен для создания пользователя.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Пользователь сервиса с авторизацией по электронной почте."""

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        """Возвращает адрес электронной почты пользователя."""
        return self.email
