from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from users.forms import UserRegisterForm, UserLoginForm


def register(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Отправка приветственного письма
            send_mail(
                subject='Добро пожаловать!',
                message=f'Здравствуйте, {user.email}!\n\n'
                       f'Вы успешно зарегистрировались в нашем магазине.\n'
                       f'Спасибо за регистрацию!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            
            messages.success(request, 'Регистрация прошла успешно! Войдите в аккаунт.')
            return redirect('users:login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя."""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.email}!')
                return redirect('catalog:home')
        else:
            messages.error(request, 'Неверный email или пароль.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})
