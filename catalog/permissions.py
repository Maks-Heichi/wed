"""Проверки прав доступа к продуктам."""


def user_can_edit_product(user, product) -> bool:
    """Проверяет, может ли пользователь редактировать продукт."""
    if not user.is_authenticated:
        return False
    if product.owner_id == user.id:
        return True
    return user.has_perm("catalog.delete_product")


def user_can_delete_product(user, product) -> bool:
    """Проверяет, может ли пользователь удалить продукт."""
    return user_can_edit_product(user, product)


def user_can_unpublish_product(user) -> bool:
    """Проверяет, может ли пользователь отменять публикацию продукта."""
    return user.is_authenticated and user.has_perm("catalog.can_unpublish_product")
