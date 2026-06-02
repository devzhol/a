from django.db import models


class Product(models.Model):

    # Название
    title = models.CharField(
        max_length=100
    )

    # Описание
    description = models.TextField()

    # Цена
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Дата создания
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Активен
    is_active = models.BooleanField(
        default=True
    )

    # Фото
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # URL товара
    website = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.title