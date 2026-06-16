"""
Example usage of batch email sending for password recovery.

This file demonstrates how to use the low-level email methods
to send batch password reset emails.
"""

from django.contrib.auth.models import User
from goo.send_email import send_batch_password_reset_emails, send_single_password_reset_email


def example_send_batch_emails():
    """
    Example 1: Send batch password reset emails to all active users.
    """
    # Get all active users with email addresses
    users = User.objects.filter(
        is_active=True,
        email__isnull=False
    ).exclude(email='')
    
    print(f"Sending password reset emails to {users.count()} users...")
    
    # Send batch emails using low-level methods
    count = send_batch_password_reset_emails(users)
    
    print(f"Successfully sent {count} emails!")


def example_send_to_specific_users():
    """
    Example 2: Send password reset emails to specific users.
    """
    # Get specific users
    users = User.objects.filter(username__in=['user1', 'user2', 'user3'])
    
    count = send_batch_password_reset_emails(users)
    print(f"Sent {count} emails to specific users")


def example_send_single_email():
    """
    Example 3: Send a single password reset email.
    """
    user = User.objects.get(username='john')
    
    result = send_single_password_reset_email(user)
    
    if result:
        print(f"Password reset email sent to {user.email}")
    else:
        print(f"Failed to send email to {user.email}")


def example_filter_by_domain():
    """
    Example 4: Send emails only to users with specific email domain.
    """
    # Get users with @example.com email addresses
    users = User.objects.filter(email__endswith='@example.com')
    
    if users.exists():
        count = send_batch_password_reset_emails(users)
        print(f"Sent {count} emails to @example.com domain")
    else:
        print("No users found with @example.com emails")


def example_usage_in_django_shell():
    """
    Example of how to use this in Django shell.
    
    Run: python manage.py shell
    
    Then execute:
    
    >>> from django.contrib.auth.models import User
    >>> from goo.send_email import send_batch_password_reset_emails
    >>> users = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')
    >>> count = send_batch_password_reset_emails(users)
    >>> print(f"Sent {count} emails")
    """
    pass


if __name__ == '__main__':
    # Note: This would need to be run within Django environment
    # For example: python manage.py shell
    
    print("Examples of batch email sending:")
    print("=" * 50)
    
    print("\n1. Send to all active users:")
    print("   users = User.objects.filter(is_active=True, email__isnull=False)")
    print("   count = send_batch_password_reset_emails(users)")
    
    print("\n2. Send to specific users:")
    print("   users = User.objects.filter(username__in=['user1', 'user2'])")
    print("   count = send_batch_password_reset_emails(users)")
    
    print("\n3. Send single email:")
    print("   user = User.objects.get(username='john')")
    print("   send_single_password_reset_email(user)")
    
    print("\n4. Using management command:")
    print("   python manage.py send_password_reset_emails")
    print("   python manage.py send_password_reset_emails --all-users")
    print("   python manage.py send_password_reset_emails --user=username")
