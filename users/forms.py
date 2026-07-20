from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'avatar', 'phone', 'country']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите страну'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['password1', 'password2', 'avatar']:
                field.widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя."""
    
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    class Meta:
        fields = ['username', 'password']
