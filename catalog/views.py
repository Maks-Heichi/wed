"""Контроллеры приложения catalog."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from catalog.forms import ContactForm
from catalog.models import Product


class ProductListView(ListView):
    """Отображает главную страницу со списком товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает все товары каталога."""
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Отображает страницу с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


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
