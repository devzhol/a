# Homework #46 - Custom User Model

## Task

Rewrite the previous profile extension that used a relation to another table.
Implement the same idea through inheritance from an abstract Django user class.

## What was implemented

- Added `CustomUser`, inherited from `django.contrib.auth.models.AbstractUser`.
- Moved the profile fields directly into the custom user model:
  - biography;
  - phone number;
  - birth date;
  - city;
  - personal website;
  - newsletter subscription flag.
- Set `AUTH_USER_MODEL = 'goo.CustomUser'` in project settings.
- Updated registration to use `CustomUserCreationForm`.
- Updated the profile list page to display users directly, without a `Profile` relation.
- Updated Django admin so the extra fields are edited on the user page.
- Removed automatic profile creation because a separate profile table is no longer used.

## Files changed

- `goo/models.py`
- `goo/forms.py`
- `goo/admin.py`
- `goo/views.py`
- `goo/signals.py`
- `goo/context_processors.py`
- `goo/settings.py`
- `templates/profiles.html`
- `goo/migrations/0001_initial.py`
- `goo/migrations/0002_profile_birth_date_profile_city_profile_phone_number_and_more.py`

## Checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```
