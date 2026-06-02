from django.shortcuts import render
from .forms import UserProfileForm


def register_view(request):

    # Если форма отправлена
    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        # Проверяем валидность
        if form.is_valid():

            # Сохраняем данные
            form.save()

            return render(request, 'success.html')

    else:

        # Пустая форма
        form = UserProfileForm()

    return render(request, 'register.html', {
        'form': form
    })