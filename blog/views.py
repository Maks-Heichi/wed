"""Контроллеры приложения blog."""

from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import BlogPostForm
from blog.models import BlogPost


class BlogPostListView(ListView):
    """Отображает список опубликованных блоговых записей."""

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Возвращает только опубликованные записи."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Отображает блоговую запись и увеличивает счётчик просмотров."""

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Возвращает запись и увеличивает количество просмотров."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class BlogPostCreateView(CreateView):
    """Создаёт новую блоговую запись."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:list")


class BlogPostUpdateView(UpdateView):
    """Редактирует существующую блоговую запись."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = "/blogs/"

    def form_valid(self, form):
        """Сохраняет запись и задаёт success_url для перехода на её страницу."""
        self.object = form.save()
        self.success_url = reverse("blog:detail", kwargs={"pk": self.object.pk})
        return super().form_valid(form)


class BlogPostDeleteView(DeleteView):
    """Удаляет блоговую запись."""

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
