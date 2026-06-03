from django.contrib import admin
from django.urls import path, include

# Главные маршруты проекта
urlpatterns = [
    path('admin/', admin.site.urls),           # Админ-панель
    path('', include('catalog.urls')),         # Подключаем маршруты приложения catalog
]
