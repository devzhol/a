# Homework #44 - Redis Caching

## Task

1. Connect Redis and use its settings/functionality for application caching.
2. Implement a simple client-side caching option.

## What was implemented

- Redis is configured as the Django cache backend in `goo/settings.py`.
- `profile_list` uses Redis through Django's cache API and stores the profile list for 5 minutes.
- The profile cache is invalidated after a new user/profile is created.
- A `/cache-demo/` JSON endpoint demonstrates server-side Redis caching.
- The home page uses `localStorage` as a simple client-side cache for the cache demo response.
- `requirements.txt` includes the `redis` Python package.

## How to run

```bash
cd goo
pip install -r requirements.txt
redis-server
python manage.py runserver
```

If Redis is not running on the default address, set `REDIS_URL`:

```bash
set REDIS_URL=redis://127.0.0.1:6379/1
python manage.py runserver
```

## Files changed

- `goo/settings.py`
- `goo/views.py`
- `goo/urls.py`
- `templates/index.html`
- `templates/profiles.html`
- `requirements.txt`

## Submission

Push the updated repository to GitHub and attach the repository link as the homework answer.
