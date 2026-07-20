from django.db import models
from django.conf import settings


class Category(models.Model):
    """Модель категории товаров."""
    
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
        help_text='Введите наименование категории'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Введите описание категории'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара."""
    
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        help_text='Введите наименование товара'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Введите описание товара'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение',
        blank=True,
        null=True,
        help_text='Загрузите изображение товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за покупку',
        help_text='Введите цену товара'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отметьте для публикации продукта'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        help_text='Владелец продукта',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]
    
    def __str__(self):
        return self.name
