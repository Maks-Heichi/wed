"""Контроллеры приложения catalog."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ContactForm
from catalog.models import Product


def home(request):
    """Отображает главную страницу со списком товаров."""
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


def product_detail(request, pk):
    """Отображает страницу с подробной информацией о товаре."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def contacts(request):
    """Отображает страницу контактов и обрабатывает форму обратной связи."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Сообщение успешно отправлено.")
            return redirect("catalog:contacts")
        messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = ContactForm()

    return render(request, "catalog/contacts.html", {"form": form})
