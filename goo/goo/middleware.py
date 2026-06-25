from django.conf import settings
from django.contrib.auth.views import redirect_to_login


class LoginRequiredMiddleware:
    allowed_exact_paths = {
        '/login/',
        '/admin/login/',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_allowed_request(request) or request.user.is_authenticated:
            return self.get_response(request)

        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)

    def is_allowed_request(self, request):
        path = request.path_info
        static_url = settings.STATIC_URL

        if path in self.allowed_exact_paths:
            return True

        return static_url and path.startswith(static_url)
