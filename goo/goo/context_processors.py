from django.contrib.auth.models import Group, User


def all_users(request):
    """Добавляет список всех пользователей и групп текущего пользователя в контекст каждого шаблона."""
    return {
        'all_users': User.objects.all(),
        'user_groups': request.user.groups.all() if request.user.is_authenticated else Group.objects.none(),
    }
