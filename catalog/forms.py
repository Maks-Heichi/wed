"""Формы приложения catalog."""

from django import forms
from django.conf import settings

from catalog.models import Product

ALLOWED_IMAGE_FORMATS = ("image/jpeg", "image/png")
MAX_IMAGE_SIZE = 5 * 1024 * 1024


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price", "is_published")

    def __init__(self, *args, user=None, **kwargs):
        """Добавляет Bootstrap-стили и сохраняет текущего пользователя."""
        self.user = user
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-control"

    def _validate_forbidden_words(self, value: str, field_label: str) -> str:
        """Проверяет отсутствие запрещённых слов в тексте поля."""
        lower_value = value.lower()
        for word in settings.FORBIDDEN_WORDS:
            if word in lower_value:
                raise forms.ValidationError(
                    f"В поле «{field_label}» запрещено использовать слово «{word}»."
                )
        return value

    def clean_name(self):
        """Проверяет название на запрещённые слова."""
        name = self.cleaned_data.get("name", "")
        return self._validate_forbidden_words(name, "наименование")

    def clean_description(self):
        """Проверяет описание на запрещённые слова."""
        description = self.cleaned_data.get("description", "")
        if description:
            return self._validate_forbidden_words(description, "описание")
        return description

    def clean_price(self):
        """Проверяет, что цена не отрицательная."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_is_published(self):
        """Проверяет право на отмену публикации продукта."""
        is_published = self.cleaned_data.get("is_published")
        if (
            self.instance.pk
            and self.instance.is_published
            and not is_published
            and not (self.user and self.user.has_perm("catalog.can_unpublish_product"))
        ):
            raise forms.ValidationError("У вас нет прав на отмену публикации продукта.")
        return is_published

    def clean_image(self):
        """Проверяет формат и размер загружаемого изображения."""
        image = self.cleaned_data.get("image")
        if not image or not hasattr(image, "content_type"):
            return image

        if image.content_type not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError(
                "Допустимые форматы изображения: JPEG и PNG."
            )

        if image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )

        return image


class ContactForm(forms.Form):
    """Форма обратной связи на странице контактов."""

    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Ваше имя",
            }
        ),
    )
    phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "phone",
                "placeholder": "Контактный телефон",
            }
        ),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "message",
                "placeholder": "Ваше сообщение",
                "rows": 4,
            }
        ),
    )

    def save(self):
        """Заглушка для совместимости с ContactView."""
        return None
