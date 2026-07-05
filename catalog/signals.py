"""Сигналы приложения catalog."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from catalog.models import Product
from catalog.services import invalidate_category_products_cache


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_category_products_cache(sender, instance, **kwargs):
    """Сбрасывает кеш списка продуктов категории при изменении товара."""
    if instance.category_id:
        invalidate_category_products_cache(instance.category_id)
