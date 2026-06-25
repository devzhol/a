# Homework #47 - Django Mixins

## Task

1. Add more complex mixin behavior, for example login requirement and one more rule.
2. Create a mixin inherited from more basic mixins.

## What was implemented

- Added `ActiveUserRequiredMixin`, inherited from Django's `LoginRequiredMixin` and `UserPassesTestMixin`.
- The mixin requires authentication and additionally allows only active users.
- Added `CachedUserListMixin`, which builds the profile/user list with Redis cache support.
- Added `ProtectedCachedUserListMixin`, inherited from the base access and cache mixins.
- Reworked the profile list page from a function view to `ProfileListView`, which uses `ProtectedCachedUserListMixin`.
- The `/profiles/` page is now protected by login and active-user checks.

## Files changed

- `goo/mixins.py`
- `goo/view_mixins.py`
- `goo/views.py`
- `goo/urls.py`
- `HOMEWORK_47_SUMMARY.md`

## How to check

```bash
cd goo
python manage.py check
```
