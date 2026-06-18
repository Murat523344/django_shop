from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Category


def home(request):
    """Контроллер для главной страницы."""
    products = Product.objects.all().select_related('category')
    
    # Обрезаем описание до 100 символов
    for product in products:
        if product.description and len(product.description) > 100:
            product.short_description = product.description[:100] + '...'
        else:
            product.short_description = product.description
    
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """Контроллер для страницы товара."""
    product = get_object_or_404(Product, id=pk)
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    """Контроллер для страницы контактов."""
    return render(request, 'catalog/contacts.html')
