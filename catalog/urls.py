from django.urls import path
from catalog import views

# Пространство имен приложения (для удобства)
app_name = 'catalog'

# Маршруты приложения catalog
urlpatterns = [
    path('', views.home, name='home'),              # Главная страница
    path('contacts/', views.contacts, name='contacts'),  # Страница контактов
]
