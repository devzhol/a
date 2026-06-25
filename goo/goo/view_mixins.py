from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache


class ActiveUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/login/'
    permission_denied_message = 'Only active users can open this page.'
    raise_exception = True

    def test_func(self):
        return self.request.user.is_active


class CachedUserListMixin:
    cache_key = 'profiles:list'
    cache_timeout = 300
    context_object_name = 'profiles'

    def get_cached_users(self):
        users = cache.get(self.cache_key)
        self.cache_hit = users is not None

        if users is None:
            User = get_user_model()
            users = list(User.objects.order_by('username'))
            cache.set(self.cache_key, users, self.cache_timeout)

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_cached_users()
        context['cache_hit'] = self.cache_hit
        return context


class ProtectedCachedUserListMixin(ActiveUserRequiredMixin, CachedUserListMixin):
    pass
