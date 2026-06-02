from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:

        # Модель, с которой связана форма
        model = UserProfile

        # Поля формы
        fields = ['name', 'age', 'email', 'password']

    # Проверка имени
    def clean_name(self):

        name = self.cleaned_data['name']

        # Если имя слишком короткое
        if len(name) < 3:
            raise forms.ValidationError(
                'Имя должно содержать минимум 3 символа'
            )

        return name

    # Проверка возраста
    def clean_age(self):

        age = self.cleaned_data['age']

        # Пользователь должен быть старше 18
        if age < 18:
            raise forms.ValidationError(
                'Возраст должен быть 18+'
            )

        return age

    # Проверка email
    def clean_email(self):

        email = self.cleaned_data['email']

        # Разрешаем только gmail
        if '@gmail.com' not in email:
            raise forms.ValidationError(
                'Разрешены только Gmail адреса'
            )

        return email

    # Общая проверка формы
    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        # Проверка длины пароля
        if password and len(password) < 6:
            raise forms.ValidationError(
                'Пароль должен быть минимум 6 символов'
            )

        return cleaned_data