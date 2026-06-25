from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.cache import cache
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CustomUserCreationForm
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .send_email import send_batch_password_reset_emails, send_single_password_reset_email
from .view_mixins import ProtectedCachedUserListMixin


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete('profiles:list')
            messages.success(request, 'Пользователь создан.')
            return redirect('profile_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


class ProfileListView(ProtectedCachedUserListMixin, TemplateView):
    template_name = 'profiles.html'


def cache_demo(request):
    cache_key = 'home:cache-demo'
    cached_data = cache.get(cache_key)
    cache_hit = cached_data is not None

    if cached_data is None:
        cached_data = {
            'message': 'Data generated on the server and saved in Redis.',
            'generated_at': timezone.now().isoformat(),
        }
        cache.set(cache_key, cached_data, 300)

    return JsonResponse({
        **cached_data,
        'server_cache_hit': cache_hit,
        'ttl_seconds': 300,
    })


@api_view(['GET'])
def sample_api(request):
    return Response({
        'title': 'Практическая работа №49',
        'module': 'Модуль 30. Разработка Web-служб REST',
        'framework': 'Django REST Framework',
        'items': [
            {'id': 1, 'name': 'DRF установлен'},
            {'id': 2, 'name': 'APIView возвращает данные'},
            {'id': 3, 'name': 'Маршрут /api/sample/ работает'},
        ],
    })


@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    if request.method in ('PUT', 'PATCH'):
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=request.method == 'PATCH',
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_list(request):
    User = get_user_model()
    users = User.objects.order_by('username')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


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

