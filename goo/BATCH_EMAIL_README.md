# Batch Email Sending - Homework #43

## Overview

This implementation demonstrates how to send batch password recovery emails using Django's **low-level email methods**. Instead of using the high-level `send_mail()` function, we use `EmailMessage` and `get_connection()` with the `send_messages()` method for efficient batch sending.

## Key Components

### 1. **send_email.py** - Core Email Module

The main module that implements batch email sending using low-level methods:

#### Functions:

**`send_batch_password_reset_emails(users)`**
- Sends password reset emails to multiple users
- Uses `get_connection()` to create a single connection
- Creates `EmailMessage` objects for each user
- Calls `connection.send_messages()` for efficient batch sending
- Returns the count of emails sent

**`send_single_password_reset_email(user)`**
- Sends a single password reset email
- Uses low-level `EmailMessage` instead of `send_mail()`
- Returns True/False based on success

**`send_batch_emails(email_list)`**
- Generic batch email sending function
- Accepts any list of `EmailMessage` objects
- Demonstrates the pattern for low-level batch sending

### 2. **Low-Level Email Methods Used**

#### `get_connection()`
```python
from django.core.mail import get_connection

connection = get_connection()  # Uses settings.EMAIL_* configuration
```
Creates a reusable connection to the mail server. This is more efficient than creating a new connection for each email.

#### `EmailMessage`
```python
from django.core.mail import EmailMessage

email = EmailMessage(
    subject='Subject',
    body='Message body',
    from_email='from@example.com',
    to=['to@example.com'],
    connection=connection  # Use the connection object
)
email.send()  # Send individual email
```

#### `send_messages()`
```python
# Send multiple emails using one connection
connection.send_messages([email1, email2, email3])
```

This is the key low-level method for batch sending. It sends all messages through a single connection, which is much more efficient than sending individually.

### 3. **Custom Password Reset View**

[goo/views.py](goo/views.py) contains `CustomPasswordResetView` that overrides Django's default behavior:

```python
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = User.objects.filter(email=email)
        
        if users.exists():
            # Use batch sending for low-level email
            send_batch_password_reset_emails(users)
        
        return redirect(self.success_url)
```

### 4. **Management Command**

[goo/management/commands/send_password_reset_emails.py](goo/management/commands/send_password_reset_emails.py)

Allows sending batch password reset emails from the command line:

```bash
# Send to all active users with email
python manage.py send_password_reset_emails

# Send to all users (including inactive)
python manage.py send_password_reset_emails --all-users

# Send to specific user
python manage.py send_password_reset_emails --user=username
```

## Configuration

### Email Settings (settings.py)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Site configuration
SITE_URL = 'http://127.0.0.1:8000/'
SITE_NAME = 'GOO - Authentication System'
```

### Email Template

[templates/password_reset_email.html](templates/password_reset_email.html)

Professional HTML email template with:
- User personalization
- Password reset link
- Clear call-to-action button
- Footer with site information

## Advantages of Low-Level Methods

| Aspect | send_mail() | EmailMessage + get_connection() |
|--------|-------------|--------------------------------|
| **Connection Reuse** | Creates new connection per email | Reuses single connection |
| **Batch Sending** | Not ideal for multiple emails | Optimized for batches |
| **Performance** | Slow for many emails | Fast and efficient |
| **Flexibility** | Limited customization | Full control over email |
| **HTML Support** | Requires text wrapping | Native support |
| **Attachments** | Supported but cumbersome | Easy to manage |

## Usage Examples

### 1. Via Web Interface

Navigate to `/password-reset/` and submit the form. The system will:
1. Find users with that email
2. Generate password reset tokens for each
3. Send batch emails using low-level methods
4. Redirect to confirmation page

### 2. Via Management Command

```bash
# Active users only
python manage.py send_password_reset_emails

# All users including inactive
python manage.py send_password_reset_emails --all-users

# Specific user
python manage.py send_password_reset_emails --user=john
```

### 3. Programmatic Usage

```python
from django.contrib.auth.models import User
from goo.send_email import send_batch_password_reset_emails

# Get users to send emails to
users = User.objects.filter(is_active=True)

# Send batch emails
count = send_batch_password_reset_emails(users)
print(f"Sent {count} emails")
```

## Email Process Flow

```
User submits email → Form validation
                    ↓
           Find users by email
                    ↓
      Create EmailMessage objects
                    ↓
      Get connection to mail server
                    ↓
      Send all messages via connection
                    ↓
           Redirect to success page
```

## Testing

To test email sending in development:

### Option 1: Console Backend
```python
# In settings.py for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails will print to console instead of sending.

### Option 2: File Backend
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'
```
Emails will be saved as files.

### Option 3: Real SMTP
Use actual Gmail credentials (as configured in settings.py).

## Key Learning Points

1. **get_connection()** - Creates a reusable mail server connection
2. **EmailMessage** - Low-level email object with full customization
3. **send_messages()** - Batch sending method for efficiency
4. **Connection Reuse** - Single connection for multiple emails is much faster
5. **Template Rendering** - HTML email templates for professional appearance
6. **Token Generation** - Django's token generator for password reset links

## Files Modified/Created

- ✅ `goo/send_email.py` - Batch email functions
- ✅ `goo/views.py` - CustomPasswordResetView
- ✅ `goo/urls.py` - URL configuration
- ✅ `goo/settings.py` - Email settings
- ✅ `templates/password_reset_email.html` - Email template
- ✅ `goo/management/commands/send_password_reset_emails.py` - Management command

## Security Considerations

1. **Email Configuration** - Credentials should use environment variables in production
2. **SITE_URL** - Should use HTTPS in production
3. **Token Security** - Django's token generator is secure and time-limited
4. **Email Verification** - Always verify users exist before sending
5. **Rate Limiting** - Consider limiting password reset attempts per user

## References

- [Django Email Documentation](https://docs.djangoproject.com/en/6.0/topics/email/)
- [EmailMessage API](https://docs.djangoproject.com/en/6.0/ref/mail/#django.core.mail.EmailMessage)
- [get_connection()](https://docs.djangoproject.com/en/6.0/ref/mail/#django.core.mail.get_connection)
