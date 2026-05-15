"""Примеры ORM-запросов для django shell."""

from catalog.models import Category, Product

cat_web = Category.objects.create(
    name="Веб-приложения",
    description="Готовые веб-приложения и шаблоны",
)
cat_micro = Category.objects.create(
    name="Микросервисы",
    description="Архитектурные шаблоны микросервисов",
)

product_crm = Product.objects.create(
    name="CRM Lite",
    description="Легкая CRM для малого бизнеса",
    price="199.00",
    category=cat_web,
)
product_auth = Product.objects.create(
    name="Auth Gateway",
    description="Сервис аутентификации",
    price="149.50",
    category=cat_micro,
)

print("Все категории:", list(Category.objects.all()))
print("Все продукты:", list(Product.objects.all()))
print(
    "Продукты категории «Веб-приложения»:",
    list(Product.objects.filter(category=cat_web)),
)
print("Категории с «бот» в названии:", list(Category.objects.filter(name__icontains="бот")))
print("Категории, отсортированные по имени:", list(Category.objects.order_by("name")))

product_crm.price = "219.00"
product_crm.save(update_fields=["price", "updated_at"])
print("Обновлённая цена CRM Lite:", product_crm.price)

deleted, _ = Product.objects.filter(pk=product_auth.pk).delete()
print("Удалено записей:", deleted)
