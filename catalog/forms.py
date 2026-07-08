from django import forms
from catalog.models import Product

# Запрещенные слова (в любом регистре)
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продуктов с валидацией."""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        """Добавляем стили Bootstrap ко всем полям."""
        super().__init__(*args, **kwargs)
        
        # Применяем стили к каждому полю
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Добавляем placeholder для каждого поля
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Введите цену товара'
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['accept'] = 'image/*'
    
    def clean_name(self):
        """Проверка названия на запрещенные слова."""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(
                        f'Название содержит запрещенное слово: "{word}".'
                    )
        return name
    
    def clean_description(self):
        """Проверка описания на запрещенные слова."""
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(
                        f'Описание содержит запрещенное слово: "{word}".'
                    )
        return description
    
    def clean_price(self):
        """Проверка, что цена не отрицательная."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной. Пожалуйста, введите положительное число.'
            )
        return price
    
    def clean(self):
        """Общая проверка формы."""
        cleaned_data = super().clean()
        # Дополнительные проверки можно добавить здесь
        return cleaned_data
