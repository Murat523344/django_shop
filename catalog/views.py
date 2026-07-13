from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from catalog.models import Product
from catalog.forms import ProductForm


class HomeView(ListView):
    """Главная страница со списком товаров (доступна всем)."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_published=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            if product.description and len(product.description) > 100:
                product.short_description = product.description[:100] + '...'
            else:
                product.short_description = product.description
        context['title'] = 'Главная страница'
        return context


class ProductListView(ListView):
    """Список всех продуктов для администрирования."""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']


class ProductDetailView(DetailView):
    """Детальная страница товара (доступна всем)."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара (только для авторизованных)."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def form_valid(self, form):
        """Автоматически назначаем владельца."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара (только владелец или модератор)."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        """Проверка прав на редактирование."""
        product = self.get_object()
        user = self.request.user
        # Владелец или модератор может редактировать
        return user == product.owner or user.has_perm('catalog.can_unpublish_product')
    
    def handle_no_permission(self):
        """Обработка отсутствия прав."""
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта.')
        return redirect('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара (только владелец или модератор)."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        """Проверка прав на удаление."""
        product = self.get_object()
        user = self.request.user
        # Владелец или модератор может удалить
        return user == product.owner or user.has_perm('catalog.delete_product')
    
    def handle_no_permission(self):
        """Обработка отсутствия прав."""
        messages.error(self.request, 'У вас нет прав для удаления этого продукта.')
        return redirect('catalog:product_list')


class ContactsView(TemplateView):
    """Страница контактов (доступна всем)."""
    template_name = 'catalog/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
