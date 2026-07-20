from django.core.cache import cache
from catalog.models import Category


def get_products_by_category(category_id, use_cache=True):
    """
    Сервисная функция для получения продуктов по категории с кешированием.
    
    Args:
        category_id: ID категории
        use_cache: Использовать ли кеш (по умолчанию True)
    
    Returns:
        QuerySet продуктов в категории
    """
    cache_key = f'category_{category_id}_products'
    
    if use_cache:
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
    
    try:
        category = Category.objects.get(id=category_id)
        products = category.products.filter(is_published=True).select_related('category')
        
        if use_cache:
            cache.set(cache_key, products, timeout=300)
        
        return products
    except Category.DoesNotExist:
        return []
