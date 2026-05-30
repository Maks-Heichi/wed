"""Маршруты приложения catalog."""

from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactView, ProductDetailView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("home/", ProductListView.as_view(), name="home_page"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
