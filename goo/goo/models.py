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


class Task(models.Model):
    title = models.CharField('Title', max_length=200)
    description = models.TextField('Description', blank=True)
    completed = models.BooleanField('Completed', default=False)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        ordering = ['completed', '-created_at']

    def __str__(self):
        return self.title
