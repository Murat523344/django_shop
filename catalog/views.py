from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from catalog.models import Product
from catalog.forms import ProductForm


class HomeView(ListView):
    """Главная страница со списком товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        """Получаем все товары с категориями."""
        return Product.objects.all().select_related('category')
    
    def get_context_data(self, **kwargs):
        """Добавляем обрезанное описание для каждого товара."""
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
    """Детальная страница товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Создание нового товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    """Редактирование товара."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    """Удаление товара."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ContactsView(TemplateView):
    """Страница контактов."""
    template_name = 'catalog/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
