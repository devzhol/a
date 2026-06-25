# Homework #47 - Django Mixins

## Task

1. Add one property to any two classes through mixins.

## What was implemented

- Added `ProfileNameMixin` with the `display_name` property.
- Connected `ProfileNameMixin` to the `Profile` model.
- Added `ProfileAdminSummaryMixin` with the `profile_summary_label` property.
- Connected `ProfileAdminSummaryMixin` to the `ProfileAdmin` admin class.
- The admin profile list now includes a short profile summary built by the mixin.

## Files changed

- `goo/mixins.py`
- `goo/models.py`
- `goo/admin.py`
- `HOMEWORK_47_SUMMARY.md`

## How to check

```bash
cd goo
python manage.py check
```
