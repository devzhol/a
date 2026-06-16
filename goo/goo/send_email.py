"""
Module for sending batch emails using Django's low-level methods.
Implements efficient batch email sending for password recovery notifications.
Uses EmailMessage and get_connection for low-level email operations.
"""

from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse


def send_batch_password_reset_emails(users):
    """
    Send password reset emails to multiple users using low-level batch methods.
    
    This function demonstrates the use of get_connection() and send_messages()
    for efficient batch email sending instead of individual send_mail() calls.
    
    Args:
        users: QuerySet or list of User objects to send password reset emails to
        
    Returns:
        int: Number of successfully sent emails
    """
    messages = []
    
    # Create a connection to the mail server (low-level method)
    connection = get_connection()
    
    for user in users:
        # Generate reset token for each user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Build reset URL
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000/')
        reset_url = f"{site_url}reset/{uid}/{token}/"
        
        # Prepare email context
        context = {
            'user': user,
            'uid': uid,
            'token': token,
            'reset_url': reset_url,
            'site_name': getattr(settings, 'SITE_NAME', 'Site'),
        }
        
        # Render email template
        email_subject = f'Восстановление пароля для {getattr(settings, "SITE_NAME", "Site")}'
        try:
            email_body = render_to_string('password_reset_email.html', context)
        except:
            # Fallback if template doesn't exist
            email_body = f"""
Здравствуйте, {user.first_name or user.username}!

Вы запросили восстановление пароля.

Для создания нового пароля перейдите по ссылке:
{reset_url}

Если вы не запрашивали восстановление пароля, проигнорируйте это письмо.

С уважением,
Администрация сайта.
"""
        
        # Create EmailMessage object (low-level method)
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            connection=connection  # Use the shared connection
        )
        email.content_subtype = 'html'
        
        messages.append(email)
    
    # Send all messages at once using low-level batch method
    if messages:
        connection.send_messages(messages)
    
    return len(messages)


def send_single_password_reset_email(user):
    """
    Send a single password reset email to a user using low-level methods.
    
    Args:
        user: User object to send password reset email to
        
    Returns:
        bool: True if email was sent successfully
    """
    try:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Build reset URL
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000/')
        reset_url = f"{site_url}reset/{uid}/{token}/"
        
        context = {
            'user': user,
            'uid': uid,
            'token': token,
            'reset_url': reset_url,
            'site_name': getattr(settings, 'SITE_NAME', 'Site'),
        }
        
        email_subject = f'Восстановление пароля для {getattr(settings, "SITE_NAME", "Site")}'
        try:
            email_body = render_to_string('password_reset_email.html', context)
        except:
            email_body = f"""
Здравствуйте, {user.first_name or user.username}!

Вы запросили восстановление пароля.

Для создания нового пароля перейдите по ссылке:
{reset_url}

Если вы не запрашивали восстановление пароля, проигнорируйте это письмо.

С уважением,
Администрация сайта.
"""
        
        # Create EmailMessage using low-level method
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = 'html'
        
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email to {user.email}: {str(e)}")
        return False


def send_batch_emails(email_list):
    """
    Generic batch email sending using low-level connection method.
    
    This is a generic function that can send any list of EmailMessage objects.
    It demonstrates the low-level get_connection() and send_messages() approach.
    
    Args:
        email_list: List of EmailMessage objects to send
        
    Returns:
        int: Number of successfully sent emails
    """
    connection = get_connection()
    
    if email_list:
        connection.send_messages(email_list)
    
    return len(email_list)
