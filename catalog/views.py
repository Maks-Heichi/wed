"""Контроллеры приложения catalog."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ContactForm, ProductForm
from catalog.models import Category, Product
from catalog.permissions import user_can_edit_product
from catalog.services import get_products_by_category


class ProductOwnerOrModeratorMixin(UserPassesTestMixin):
    """Разрешает доступ владельцу продукта или модератору."""

    def test_func(self):
        """Проверяет права текущего пользователя на продукт."""
        product = self.get_object()
        return user_can_edit_product(self.request.user, product)


class ProductListView(ListView):
    """Отображает главную страницу со списком опубликованных товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает только опубликованные товары."""
        return Product.objects.filter(is_published=True)


class CategoryProductListView(ListView):
    """Отображает список опубликованных товаров выбранной категории."""

    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_category(self) -> Category:
        """Возвращает категорию по id из URL."""
        return get_object_or_404(Category, pk=self.kwargs["category_id"])

    def get_queryset(self):
        """Возвращает продукты категории через сервис с кешированием."""
        category = self.get_category()
        return get_products_by_category(category_id=category.pk)

    def get_context_data(self, **kwargs):
        """Добавляет объект категории в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает страницу с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        """Возвращает товары, доступные текущему пользователю."""
        user = self.request.user
        if user.has_perm("catalog.delete_product"):
            return Product.objects.all()
        queryset = Product.objects.filter(is_published=True)
        if user.is_authenticated:
            queryset = queryset | Product.objects.filter(owner=user)
        return queryset.distinct()


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создаёт новый продукт и привязывает его к текущему пользователю."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_kwargs(self):
        """Передаёт текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Сохраняет продукт с владельцем — текущим пользователем."""
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан.")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerOrModeratorMixin, UpdateView):
    """Редактирует продукт, если пользователь является владельцем или модератором."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_form_kwargs(self):
        """Передаёт текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Сохраняет продукт и перенаправляет на страницу товара."""
        self.object = form.save()
        self.success_url = reverse("catalog:product_detail", kwargs={"pk": self.object.pk})
        messages.success(self.request, "Продукт успешно обновлён.")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, ProductOwnerOrModeratorMixin, DeleteView):
    """Удаляет продукт, если пользователь является владельцем или модератором."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт после успешной проверки прав."""
        messages.success(self.request, "Продукт удалён.")
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Отменяет публикацию продукта для пользователей с соответствующим правом."""

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        """Снимает продукт с публикации."""
        product = get_object_or_404(Product, pk=pk)
        if not product.is_published:
            messages.info(request, "Продукт уже не опубликован.")
            return redirect("catalog:home")

        product.is_published = False
        product.save(update_fields=["is_published"])
        messages.success(request, "Публикация продукта отменена.")
        return redirect("catalog:home")


class ContactView(View):
    """Отображает страницу контактов и обрабатывает форму обратной связи."""

    template_name = "catalog/contacts.html"

    def get(self, request):
        """Отображает форму обратной связи."""
        return render(request, self.template_name, {"form": ContactForm()})

    def post(self, request):
        """Проверяет и сохраняет сообщение из формы."""
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сообщение успешно отправлено.")
            return redirect("catalog:contacts")
        messages.error(request, "Исправьте ошибки в форме.")
        return render(request, self.template_name, {"form": form})
