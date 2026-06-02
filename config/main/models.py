from django.db import models


class UserProfile(models.Model):

    # Имя пользователя
    name = models.CharField(max_length=100)

    # Возраст пользователя
    age = models.IntegerField()

    # Электронная почта
    email = models.EmailField()

    # Пароль
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name