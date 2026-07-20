from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from catalog.models import Product, Category
from catalog.forms import ProductForm
from catalog.services import get_products_by_category


class HomeView(ListView):
    """Главная страница со списком товаров."""
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
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    """Список всех продуктов для администрирования."""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    """Детальная страница товара с кешированием."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.can_unpublish_product')
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта.')
        return redirect('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.delete_product')
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого продукта.')
        return redirect('catalog:product_list')


class CategoryProductsView(ListView):
    """Список продуктов в категории с кешированием."""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        context['title'] = f'Товары категории: {category.name}'
        return context


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
