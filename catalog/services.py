"""Сервисные функции для работы с продуктами каталога."""

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from catalog.models import Category, Product


def get_category_cache_key(category_id: int) -> str:
    """Возвращает ключ кеша для списка продуктов категории."""
    return f"category_{category_id}"


def get_products_by_category(category_id: int):
    """
    Возвращает список опубликованных продуктов указанной категории.

    Данные кешируются в Redis с ключом category_{id} и TTL из настроек.
    """
    get_object_or_404(Category, pk=category_id)

    cache_key = get_category_cache_key(category_id)
    products = cache.get(cache_key)
    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True,
            ).select_related("category")
        )
        cache.set(cache_key, products, timeout=settings.CACHE_TTL_CATEGORY_PRODUCTS)
    return products


def invalidate_category_products_cache(category_id: int) -> None:
    """Удаляет из кеша список продуктов категории."""
    cache.delete(get_category_cache_key(category_id))
