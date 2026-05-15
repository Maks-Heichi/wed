from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Очищает каталог и загружает тестовые данные из фикстур."""

    help = "Удаляет категории и продукты, затем загружает фикстуры categories и products."

    def handle(self, *args, **options):
        """Удаляет записи каталога и вызывает loaddata."""
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()

        call_command("loaddata", "categories", "products", verbosity=options["verbosity"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Удалено: продуктов — {deleted_products}, категорий — {deleted_categories}. "
                f"Загружено категорий — {Category.objects.count()}, "
                f"продуктов — {Product.objects.count()}."
            )
        )
