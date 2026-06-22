"""Настройки административной панели для приложения blog."""

from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Отображение блоговых записей в административной панели."""

    list_display = ("id", "title", "is_published", "views_count", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
