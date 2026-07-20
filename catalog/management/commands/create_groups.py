from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    """Кастомная команда для создания групп и назначения прав."""
    
    help = 'Создает группы и назначает права'

    def handle(self, *args, **options):
        self.stdout.write('Создание групп и прав...')
        
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')
        
        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # Получаем права
        # Право на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=product_content_type
        )
        self.stdout.write(f'Право can_unpublish_product: {unpublish_perm.name}')
        
        # Право на удаление продукта
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type
        )
        
        # Назначаем права группе
        moderator_group.permissions.add(unpublish_perm, delete_perm)
        self.stdout.write('Права назначены группе "Модератор продуктов"')
        
        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы!'))
