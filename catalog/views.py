"""Контроллеры приложения catalog."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
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
from catalog.models import Product


class ProductListView(ListView):
    """Отображает главную страницу со списком товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает все товары каталога."""
        return Product.objects.all()


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает страницу с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создаёт новый продукт."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует существующий продукт."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        """Сохраняет продукт и перенаправляет на страницу товара."""
        self.object = form.save()
        self.success_url = reverse("catalog:product_detail", kwargs={"pk": self.object.pk})
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет продукт."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


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
