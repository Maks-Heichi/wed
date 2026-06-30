from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создаёт группу модераторов продуктов с необходимыми правами."""

    help = "Создаёт группу «Модератор продуктов» и назначает ей права на модерацию."

    def handle(self, *args, **options):
        """Создаёт или обновляет группу модераторов."""
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            content_type__model="product",
            codename__in=("can_unpublish_product", "delete_product"),
        )
        group.permissions.set(permissions)

        action = "создана" if created else "обновлена"
        self.stdout.write(
            self.style.SUCCESS(
                f"Группа «Модератор продуктов» {action}. "
                f"Назначено прав: {permissions.count()}."
            )
        )
