# Домашнее задание № 37: Модуль 20 - Обработка выгруженных файлов

## 📋 Описание задания

Реализовать функциональность загрузки файлов (xlsx, pdf) в Django проекте `todo_api`:

1. ✅ Подготовить поле для хранения xlsx/pdf файлов
2. ✅ Добавить вывод формы на фронтенд
3. ✅ Настроить обслуживание медиа-файлов

## 🎯 Реализованные изменения

### 1. Модель Document (`tasks/models.py`)

Создана новая модель `Document` с полями:

```python
class Document(models.Model):
    title = models.CharField(max_length=200)                    # Название документа
    description = models.TextField(blank=True)                  # Описание
    file = models.FileField(upload_to='documents/',              # Файл с валидацией
                           validators=[FileExtensionValidator(allowed_extensions=['pdf', 'xlsx'])])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Кто загрузил
    uploaded_at = models.DateTimeField(auto_now_add=True)       # Когда загрузили
```

**Особенности:**
- Валидация расширений файлов (.pdf, .xlsx)
- Автоматическое отслеживание пользователя и даты загрузки
- Сортировка по дате загрузки (новые вверху)
- Русские названия полей для администраторского интерфейса

### 2. Конфигурация Django (`todo_api/settings.py`)

Добавлены настройки для работы с медиа-файлами:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 3. URL конфигурация (`todo_api/urls.py`)

Добавлена обработка медиа-файлов в режиме разработки:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4. Форма DocumentUploadForm (`tasks/forms.py`)

```python
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.xlsx'}),
        }
```

**Особенности:**
- Bootstrap стили (class='form-control')
- Ограничение выбора файлов в диалоге (.pdf, .xlsx)
- Удобные placeholder тексты
- Поддержка опционального описания

### 5. Views (`tasks/views.py`)

#### DocumentUploadView
- GET: Отображение формы загрузки
- POST: Обработка загруженного файла
- Защита: требуется авторизация (@login_required)
- Автоматическое сохранение текущего пользователя как `uploaded_by`

#### DocumentListView
- Отображение списка всех загруженных документов
- Пагинация (10 документов на странице)
- Показ информации: название, описание, автор, дата
- Возможность скачать файл напрямую

### 6. Шаблоны

#### `templates/document_upload.html`
- Красивая форма загрузки документов
- Валидация на фронтенде (accept=".pdf,.xlsx")
- Информационное сообщение о поддерживаемых форматах
- Обработка ошибок валидации
- Навигационные кнопки

#### `templates/document_list.html`
- Таблица загруженных документов
- Эмодзи для визуального обозначения типа файла (📄 PDF, 📊 XLSX)
- Пагинация с навигацией
- Кнопка скачивания документа
- Сообщение "Документы не найдены" если список пуст
- Быстрая ссылка на загрузку нового документа

### 7. Администраторский интерфейс (`tasks/admin.py`)

Зарегистрирована модель `Document` в админ-панели с:
- Отображением: название, автор, дата, файл
- Фильтрацией по дате и автору
- Поиском по названию и описанию
- Автоматическим указанием текущего пользователя при создании

### 8. Навигация (`templates/base.html`)

Добавлена ссылка на раздел документов в главное меню:
```html
<a class="nav-link d-inline" href="/documents/">📁 Документы</a>
```

### 9. URL маршруты (`tasks/urls.py`)

```python
path('documents/upload/', DocumentUploadView.as_view(), name='document_upload'),  # /documents/upload/
path('documents/', DocumentListView.as_view(), name='document_list'),             # /documents/
```

### 10. Миграция базы данных

Создана и применена миграция `0005_document_userprofile.py`:
- Создает таблицу `Document` с необходимыми полями
- Устанавливает связь с таблицей пользователей
- Настраивает индексы для оптимизации

## 📁 Структура файлов

```
todo_api/
├── manage.py
├── db.sqlite3
├── media/                          # Папка для загруженных файлов
│   └── documents/                  # Документы
├── templates/
│   ├── base.html                   # Обновлено
│   ├── document_upload.html        # ✨ НОВОЕ
│   └── document_list.html          # ✨ НОВОЕ
├── tasks/
│   ├── models.py                   # Обновлено (добавлена модель Document)
│   ├── forms.py                    # Обновлено (добавлена форма DocumentUploadForm)
│   ├── views.py                    # Обновлено (добавлены 2 новых view)
│   ├── urls.py                     # Обновлено (добавлены 2 маршрута)
│   ├── admin.py                    # Обновлено (зарегистрирована Document)
│   └── migrations/
│       └── 0005_document_userprofile.py  # ✨ НОВОЕ
├── todo_api/
│   ├── settings.py                 # Обновлено (MEDIA конфигурация)
│   ├── urls.py                     # Обновлено (static media urls)
│   └── ...
└── ...
```

## 🚀 Использование

### 1. Загрузка документа

1. Авторизуйтесь на сайте
2. Нажмите "📁 Документы" в меню
3. Кликните "➕ Загрузить новый документ"
4. Заполните форму:
   - **Название**: Укажите название документа
   - **Описание** (опционально): Добавьте описание
   - **Файл**: Выберите файл .pdf или .xlsx
5. Нажмите "✓ Загрузить документ"

### 2. Просмотр документов

1. Перейдите на страницу "📁 Документы"
2. Просмотрите список всех загруженных файлов
3. Нажмите "⬇️ Скачать" для скачивания файла

### 3. Админ-панель

1. Перейдите на `/admin/`
2. Найдите раздел "Документы"
3. Просмотрите, отредактируйте или удалите документы

## 🔒 Безопасность

- ✅ Валидация расширений файлов (.pdf, .xlsx только)
- ✅ Проверка авторизации (@login_required)
- ✅ CSRF защита ({% csrf_token %})
- ✅ Автоматическое сохранение информации об авторе загрузки

## 📝 Примеры кода

### Загрузка через форму

```python
from django.shortcuts import redirect, render
from django.views import View
from .forms import DocumentUploadForm

class DocumentUploadView(View):
    def post(self, request):
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_list')
```

### Использование в шаблоне

```html
<a href="{{ document.file.url }}" download>
    Скачать
</a>
```

## ✨ Дополнительные возможности

- 📊 Пагинация списка документов
- 🔍 Поиск и фильтрация в админ-панели
- 📱 Адаптивный дизайн (Bootstrap 5)
- 🎨 Иконки для типов файлов
- 📅 Отсортированы по дате (новые первыми)

## 🔗 Развертывание

Для развертывания в production:

```python
# settings.py
DEBUG = False
MEDIA_URL = '/media/'  # Используйте nginx или S3 для production
```

## 📄 Лицензия

Этот проект является домашним заданием для курса Django.

---

**Разработано:** GitHub Copilot  
**Дата:** Июнь 2026  
**Проект:** todo_api  
**Модуль:** 20 - Обработка файлов
