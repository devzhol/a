from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def clear_user_list_cache(sender, instance, **kwargs):
    cache.delete('profiles:list')
