# Homework #49 - Django REST Framework

## Task

1. Add routes and function controllers for a todo-list application.
2. Add logic that returns an array of users through DRF.

## What was implemented

- Added the `Task` model for todo-list items.
- Added `TaskSerializer` and `UserSerializer`.
- Added DRF function-based controllers:
  - `task_list` for listing and creating tasks;
  - `task_detail` for reading, updating, partially updating, and deleting one task;
  - `user_list` for returning an array of users.
- Registered `Task` in the Django admin panel.

## API routes

```text
GET    /api/tasks/
POST   /api/tasks/
GET    /api/tasks/<id>/
PUT    /api/tasks/<id>/
PATCH  /api/tasks/<id>/
DELETE /api/tasks/<id>/
GET    /api/users/
```

## Example task payload

```json
{
  "title": "Learn DRF",
  "description": "Create function-based API views",
  "completed": false
}
```

## Checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```
