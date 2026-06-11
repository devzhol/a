from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core import signing
from django.shortcuts import redirect, render

from .models import Profile


def home(request):
    signed_payload = signing.dumps({
        'page': 'home',
        'user': request.user.username if request.user.is_authenticated else 'guest',
    })
    return render(request, 'index.html', {'signed_payload': signed_payload})


def show_message(request):
    messages.success(request, 'Всплывающее сообщение успешно отправлено!')
    return redirect('home')


def show_warning_message(request):
    messages.warning(request, 'Отдельный уровень уведомления был вызван.')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пользователь создан. Профиль автоматически добавлен.')
            return redirect('profile_list')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def profile_list(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'profiles.html', {'profiles': profiles})
