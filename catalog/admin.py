from django.contrib import admin

from catalog.models import Category, ContactMessage, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в административной панели."""

    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение продуктов в административной панели."""

    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Отображение сообщений обратной связи."""

    list_display = ("id", "name", "phone", "created_at")
    search_fields = ("name", "phone", "message")
