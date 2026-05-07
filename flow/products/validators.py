from django.core.exceptions import ValidationError


def positive_validator(value):
    if value < 0:
        raise ValidationError(
            'Разрешены только положительные числа и 0'
        )