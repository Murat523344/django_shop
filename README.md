# Интернет-магазин на Django

## Описание проекта
Проект интернет-магазина, разрабатываемый в рамках курса. Включает каталог товаров и страницу с контактной информацией.

## Технологии
- Python 3.9+
- Django 4.2+
- Bootstrap 5

## Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd django_shop

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# venv\Scripts\activate  # для Windows

# Установка зависимостей
pip install -r requirements.txt

# Выполнение миграций
python manage.py migrate

# Запуск сервера
python manage.py runserver
Структура проекта

catalog/ - приложение каталога
config/ - настройки проекта
templates/ - HTML шаблоны
Функционал

Главная страница
Страница контактов
text

## Шаг 4: Создаем Django проект

```bash
# Создаем проект
django-admin startproject config .

# Создаем приложение catalog
python manage.py startapp catalog
## Pull Request
