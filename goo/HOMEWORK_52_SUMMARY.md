# Homework #52 - DRF Authentication Protection

## Task

1. Protect the system so all pages are available only to authenticated users.
2. Keep the login route open to all requests, otherwise users cannot sign in.

## What was implemented

- Added `LoginRequiredMiddleware`.
- The middleware redirects every anonymous request to `/login/`.
- The `/login/` route is explicitly allowed without authentication.
- Static files and `/admin/login/` are also allowed so the login forms can load.
- Added `/logout/` through Django's built-in `LogoutView`.
- Added `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL` settings.

## Routes

```text
GET  /login/
POST /login/
POST /logout/
```

All other project pages and DRF endpoints require an authenticated user.

## Checks

```bash
python manage.py check
```
