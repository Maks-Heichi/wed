from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в административной панели."""

    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение продуктов в административной панели."""

    list_display = ("id", "name", "price", "category", "owner", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("name", "description")
