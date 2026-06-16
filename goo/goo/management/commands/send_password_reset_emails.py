"""
Management command to send batch password reset emails to all users.

This demonstrates the use of low-level email methods (EmailMessage and
get_connection with send_messages) for efficient batch email sending.

Usage:
    python manage.py send_password_reset_emails
    python manage.py send_password_reset_emails --all-users
    python manage.py send_password_reset_emails --user=username
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from goo.send_email import send_batch_password_reset_emails, send_single_password_reset_email


User = get_user_model()


class Command(BaseCommand):
    help = 'Send batch password reset emails to users using low-level email methods'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all-users',
            action='store_true',
            help='Send password reset emails to all users with email addresses',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Send password reset email to a specific user by username',
        )
        parser.add_argument(
            '--inactive',
            action='store_true',
            help='Include inactive users when sending batch emails',
        )

    def handle(self, *args, **options):
        if options['user']:
            # Send to specific user
            try:
                user = User.objects.get(username=options['user'])
                result = send_single_password_reset_email(user)
                if result:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Письмо для восстановления пароля отправлено пользователю: {user.username}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'✗ Ошибка при отправке письма пользователю: {user.username}'
                        )
                    )
            except User.DoesNotExist:
                raise CommandError(f'Пользователь "{options["user"]}" не найден')
        else:
            # Send to all or active users
            if options['all_users']:
                users = User.objects.filter(email__isnull=False).exclude(email='')
            else:
                users = User.objects.filter(
                    is_active=True,
                    email__isnull=False
                ).exclude(email='')

            if not users.exists():
                self.stdout.write(self.style.WARNING('Не найдено пользователей с email адресами'))
                return

            user_count = users.count()
            self.stdout.write(f'Отправка писем для восстановления пароля {user_count} пользователям...')

            # Send batch emails using low-level methods
            try:
                count = send_batch_password_reset_emails(users)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Успешно отправлено {count} писем для восстановления пароля'
                    )
                )
            except Exception as e:
                raise CommandError(f'Ошибка при отправке писем: {str(e)}')
