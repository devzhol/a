from django.contrib.auth.models import AbstractUser
from django.db import models

from .mixins import ProfileNameMixin


class CustomUser(ProfileNameMixin, AbstractUser):
    bio = models.TextField('About user', blank=True)
    phone_number = models.CharField('Phone number', max_length=20, blank=True)
    birth_date = models.DateField('Birth date', null=True, blank=True)
    city = models.CharField('City', max_length=100, blank=True)
    website = models.URLField('Website', blank=True)
    receive_newsletter = models.BooleanField('Receive newsletter', default=True)

    def __str__(self):
        return self.display_name
