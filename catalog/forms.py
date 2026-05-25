"""Формы приложения catalog."""

from django import forms

from catalog.models import ContactMessage


class ContactForm(forms.ModelForm):
    """Форма обратной связи на странице контактов."""

    class Meta:
        model = ContactMessage
        fields = ("name", "phone", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "name",
                    "placeholder": "Ваше имя",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "phone",
                    "placeholder": "Контактный телефон",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "message",
                    "placeholder": "Ваше сообщение",
                    "required": True,
                    "rows": 4,
                }
            ),
        }

    def clean_name(self):
        """Проверяет, что имя заполнено и не состоит из пробелов."""
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Укажите имя.")
        return name

    def clean_phone(self):
        """Проверяет, что телефон заполнен и не состоит из пробелов."""
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            raise forms.ValidationError("Укажите телефон.")
        return phone

    def clean_message(self):
        """Проверяет, что текст сообщения заполнен."""
        message = self.cleaned_data.get("message", "").strip()
        if not message:
            raise forms.ValidationError("Введите сообщение.")
        return message
