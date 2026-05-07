from django.db import models
from .validators import positive_validator


class Product(models.Model):
    name = models.CharField(max_length=100)

    price = models.IntegerField(
        validators=[positive_validator]
    )

    quantity = models.IntegerField(
        validators=[positive_validator]
    )

    def __str__(self):
        return self.name

    # id + значение
    def get_product_info(self):
        return f"{self.id} - {self.name}"

    # сумма значений
    def get_total_price(self):
        return self.price * self.quantity