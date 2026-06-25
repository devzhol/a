# Практическая работа №49

## Тема

Модуль 30. Разработка Web-служб REST. REST framework. Django REST Framework.

## Что сделано

- В проект добавлена библиотека `djangorestframework`.
- В `INSTALLED_APPS` подключено приложение `rest_framework`.
- Создан простой DRF endpoint, который возвращает данные в формате JSON.
- Добавлен маршрут:

```text
GET /api/sample/
```

## Пример ответа

```json
{
  "title": "Практическая работа №49",
  "module": "Модуль 30. Разработка Web-служб REST",
  "framework": "Django REST Framework",
  "items": [
    {
      "id": 1,
      "name": "DRF установлен"
    },
    {
      "id": 2,
      "name": "APIView возвращает данные"
    },
    {
      "id": 3,
      "name": "Маршрут /api/sample/ работает"
    }
  ]
}
```

## Как проверить

```bash
pip install -r requirements.txt
python manage.py runserver
```

Откройте в браузере:

```text
http://127.0.0.1:8000/api/sample/
```
