from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core import signing
from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import Profile
from .send_email import send_batch_password_reset_emails, send_single_password_reset_email


def home(request):
    signed_payload = signing.dumps({
        'page': 'home',
        'user': request.user.username if request.user.is_authenticated else 'guest',
    })
    return render(request, 'index.html', {'signed_payload': signed_payload})


def show_message(request):
    messages.success(request, 'Всплывающее сообщение успешно отправлено!')
    return redirect('home')


def show_warning_message(request):
    messages.warning(request, 'Отдельный уровень уведомления был вызван.')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for new user
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Пользователь создан. Профиль автоматически добавлен.')
            return redirect('profile_list')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def profile_list(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'profiles.html', {'profiles': profiles})


class CustomPasswordResetView(PasswordResetView):
    """
    Custom Password Reset View using batch email sending (low-level methods).
    
    This view demonstrates sending password reset emails using Django's
    low-level email methods (EmailMessage and get_connection with send_messages)
    instead of the high-level send_mail function.
    """
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        """
        Override form_valid to use batch email sending.
        """
        # Get the user's email from the form
        email = form.cleaned_data['email']
        
        # Find user(s) with this email
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.filter(email=email)
        
        if users.exists():
            # Send batch password reset emails using low-level methods
            send_batch_password_reset_emails(users)
        
        # Return success response (don't reveal if email exists)
        return redirect(self.success_url)


def send_batch_password_reset_emails_view(request):
    """
    Admin view to send batch password reset emails to multiple users.
    
    This demonstrates the use of batch email sending for password recovery.
    In production, this should be restricted to admin users.
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get all users with email
        users = User.objects.filter(email__isnull=False).exclude(email='')
        
        # Send batch emails using low-level methods
        count = send_batch_password_reset_emails(users)
        
        messages.success(request, f'Отправлено писем для восстановления пароля: {count}')
        return redirect('admin:index')
    except Exception as e:
        messages.error(request, f'Ошибка при отправке писем: {str(e)}')
        return redirect('admin:index')

