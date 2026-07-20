from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blog.models import BlogPost


class BlogListView(ListView):
    """Список опубликованных статей."""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        """Выводим только опубликованные статьи."""
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Детальная страница статьи."""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при открытии статьи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    """Создание новой статьи."""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    """Редактирование статьи."""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    
    def get_success_url(self):
        """Перенаправляем на просмотр отредактированной статьи."""
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление статьи."""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
