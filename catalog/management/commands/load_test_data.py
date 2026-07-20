from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает тестовые данные'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка тестовых данных...')
        
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write('Существующие данные удалены')
        
        cat1 = Category.objects.create(name='Электроника', description='Смартфоны, ноутбуки')
        cat2 = Category.objects.create(name='Одежда', description='Мужская и женская одежда')
        cat3 = Category.objects.create(name='Книги', description='Художественная литература')
        
        self.stdout.write(f'Созданы категории: {cat1.name}, {cat2.name}, {cat3.name}')
        
        Product.objects.create(name='iPhone 15', description='Флагманский смартфон', category=cat1, price=99999)
        Product.objects.create(name='MacBook Pro', description='Мощный ноутбук', category=cat1, price=199999)
        Product.objects.create(name='Джинсы', description='Классические джинсы', category=cat2, price=4999)
        
        self.stdout.write('Продукты созданы')
        
        electronics_products = Product.objects.filter(category=cat1)
        self.stdout.write(f'Продуктов в категории Электроника: {electronics_products.count()}')
        
        self.stdout.write(self.style.SUCCESS('Загрузка завершена!'))
