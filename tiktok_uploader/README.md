# TikTok Uploader Module

## 📋 Описание

Модуль автоматизации TikTok, созданный по аналогии с Instagram Uploader. Предоставляет полный функционал для управления TikTok аккаунтами и массовой загрузки контента.

## 🏗️ Архитектура

### Структура проекта

```
tiktok_uploader/
├── __init__.py                  # Инициализация приложения
├── apps.py                      # Конфигурация Django приложения
├── models.py                    # Модели данных (аккаунты, задачи, прокси)
├── views.py                     # Основные представления (аккаунты, dashboard)
├── views_warmup.py              # Представления для прогрева аккаунтов
├── views_follow.py              # Представления для подписок/отписок
├── views_mod/                   # Модульные представления
│   ├── __init__.py
│   ├── views_bulk.py            # Массовая загрузка видео
│   ├── views_proxies.py         # Управление прокси
│   └── views_cookie.py          # Управление cookies
├── urls.py                      # URL маршруты
├── forms.py                     # Django формы
├── admin.py                     # Админ панель
└── README.md                    # Документация
```

## 🚀 Быстрый старт

### 1. Миграции базы данных

```bash
python manage.py makemigrations tiktok_uploader
python manage.py migrate
```

### 2. Создание суперпользователя (если нужно)

```bash
python manage.py createsuperuser
```

### 3. Запуск сервера

```bash
python manage.py runserver
```

### 4. Доступ к приложению

- **TikTok Dashboard**: http://localhost:8000/tiktok/
- **Admin Panel**: http://localhost:8000/admin/

## 📊 Основные модули

### 1. Управление аккаунтами (`/tiktok/accounts/`)

**Функционал:**
- Список всех TikTok аккаунтов
- Создание и импорт аккаунтов
- Редактирование данных аккаунта
- Привязка прокси
- Создание Dolphin Anty профилей
- Массовые операции

**Модели:**
- `TikTokAccount` - основные данные аккаунта
- `DolphinProfileSnapshot` - снимок Dolphin профиля

### 2. Управление прокси (`/tiktok/proxies/`)

**Функционал:**
- Список прокси с статусами
- Добавление и импорт прокси
- Тестирование прокси
- Смена IP через API
- Автоматическая валидация
- Определение геолокации

**Модель:**
- `TikTokProxy` - данные прокси-сервера

### 3. Массовая загрузка видео (`/tiktok/bulk-upload/`)

**Функционал:**
- Создание задач загрузки
- Добавление видео (drag & drop)
- Загрузка описаний из файла
- Настройка privacy, comments, duet, stitch
- Асинхронная загрузка через Celery
- Real-time мониторинг прогресса
- Логи выполнения

**Модели:**
- `BulkUploadTask` - задача загрузки
- `BulkUploadAccount` - привязка аккаунта к задаче
- `BulkVideo` - видео для загрузки
- `VideoCaption` - описания видео

**Процесс загрузки:**
1. Открывает Dolphin профиль
2. Логинится в TikTok
3. Переходит на /upload
4. Загружает видео
5. Заполняет описание и хештеги
6. Настраивает опции
7. Публикует
8. Логирует результат

### 4. Прогрев аккаунтов (`/tiktok/warmup/`)

**Функционал:**
- Имитация активности реального пользователя
- Настраиваемые диапазоны действий:
  - Прокрутка ленты For You
  - Просмотр видео
  - Лайки
  - Подписки
  - Комментарии
- Параллельная обработка (до 4 аккаунтов)
- Human-like поведение

**Модели:**
- `WarmupTask` - задача прогрева
- `WarmupTaskAccount` - привязка аккаунта

### 5. Подписки и отписки (`/tiktok/follow/`)

**Функционал:**
- Категории целевых аккаунтов
- Подписка на подписчиков целевых аккаунтов
- Массовые отписки
- Фильтрация ботов и подозрительных аккаунтов
- Настраиваемые лимиты

**Модели:**
- `FollowCategory` - категория целей
- `FollowTarget` - целевой аккаунт
- `FollowTask` - задача подписок
- `FollowTaskAccount` - привязка аккаунта

### 6. Управление cookies (`/tiktok/cookies/`)

**Функционал:**
- Автоматическое обновление cookies
- Синхронизация с Dolphin профилями
- Импорт/экспорт cookies
- Валидация срока действия
- Использование для API загрузки

**Модели:**
- `CookieRobotTask` - задача обновления
- `CookieRobotTaskAccount` - привязка аккаунта

## 🔧 API эндпоинты

### Основные эндпоинты

| URL | Метод | Описание |
|-----|-------|----------|
| `/tiktok/` | GET | Главный dashboard |
| `/tiktok/accounts/` | GET | Список аккаунтов |
| `/tiktok/accounts/create/` | GET/POST | Создание аккаунта |
| `/tiktok/accounts/import/` | POST | Импорт аккаунтов |
| `/tiktok/proxies/` | GET | Список прокси |
| `/tiktok/bulk-upload/` | GET | Список задач загрузки |
| `/tiktok/bulk-upload/create/` | POST | Создание задачи |
| `/tiktok/bulk-upload/<id>/start-api/` | POST | Запуск загрузки |
| `/tiktok/warmup/` | GET | Список задач прогрева |
| `/tiktok/follow/` | GET | Подписки |
| `/tiktok/cookies/` | GET | Cookie dashboard |

### API для мониторинга

| URL | Описание |
|-----|----------|
| `/tiktok/api/stats/` | Общая статистика |
| `/tiktok/api/account/<id>/status/` | Статус аккаунта |
| `/tiktok/api/task/<id>/progress/` | Прогресс задачи |
| `/tiktok/bulk-upload/<id>/logs/` | Логи задачи (real-time) |

## 🎯 Использование

### Создание задачи массовой загрузки

```python
# 1. Создайте аккаунты
from tiktok_uploader.models import TikTokAccount

account = TikTokAccount.objects.create(
    username="your_username",
    password="your_password",
    email="your_email@example.com",
    status="ACTIVE"
)

# 2. Создайте задачу через веб-интерфейс или API
# /tiktok/bulk-upload/create/

# 3. Добавьте видео
# /tiktok/bulk-upload/<task_id>/add-videos/

# 4. Добавьте описания
# /tiktok/bulk-upload/<task_id>/add-captions/

# 5. Запустите загрузку
# POST /tiktok/bulk-upload/<task_id>/start-api/
```

### Прогрев аккаунта

```python
from tiktok_uploader.models import WarmupTask, WarmupTaskAccount

# Создайте задачу прогрева
task = WarmupTask.objects.create(
    name="Warmup New Accounts",
    delay_min_sec=15,
    delay_max_sec=45,
    feed_scroll_min_count=5,
    feed_scroll_max_count=15,
    like_min_count=3,
    like_max_count=10,
)

# Добавьте аккаунты
WarmupTaskAccount.objects.create(task=task, account=account)

# Запустите через веб-интерфейс
# POST /tiktok/warmup/<task_id>/start/
```

## ⚙️ Конфигурация

### Переменные окружения

```bash
# Dolphin Anty API
DOLPHIN_API_TOKEN=your_dolphin_api_token

# База данных
DATABASE_URL=postgresql://user:password@localhost/dbname

# Celery (для асинхронных задач)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Настройки в settings.py

```python
# Добавьте в INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'tiktok_uploader',
]

# Настройки загрузки файлов
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

## 🔒 Безопасность

### Антидетект механизмы

1. **Dolphin Anty интеграция**
   - Уникальные fingerprints для каждого аккаунта
   - Реалистичные User-Agents
   - Canvas и WebGL fingerprints

2. **Human-like поведение**
   - Случайные задержки между действиями
   - Плавные движения мыши (Bézier curves)
   - Имитация чтения контента
   - Вариативность действий

3. **Прокси менеджмент**
   - Привязка прокси к аккаунтам
   - Ротация IP
   - Геолокация прокси

4. **Обработка ошибок**
   - CAPTCHA detection и уведомления
   - Rate limit handling
   - Автоматические retry

## 📝 TODO: Реализация функций

⚠️ **ВАЖНО**: Все функции в модуле пока **пустые** (только с документацией). Необходимо реализовать:

### Приоритет 1 (Критичные):
- [ ] Базовая авторизация в TikTok через Playwright
- [ ] Загрузка одного видео через браузер
- [ ] Создание Dolphin профиля для аккаунта
- [ ] Тестирование прокси

### Приоритет 2 (Важные):
- [ ] Массовая загрузка видео (worker)
- [ ] Асинхронная обработка через Celery
- [ ] Real-time логи через WebSocket
- [ ] Прогрев аккаунтов (базовые действия)

### Приоритет 3 (Дополнительные):
- [ ] Подписки/отписки
- [ ] Управление cookies
- [ ] Автоматическая валидация прокси
- [ ] Статистика и аналитика

## 🛠️ Разработка

### Структура пустых функций

Каждая функция содержит полную документацию:
- Описание назначения
- Параметры (Args)
- Возвращаемые значения (Returns)
- Процесс выполнения (Process)
- Примеры использования

Пример:
```python
def upload_video(request, video_id):
    """
    Загрузка видео на TikTok.
    
    Args:
        request: HTTP запрос
        video_id (int): ID видео
    
    Process:
        1. Открыть Dolphin профиль
        2. Логин в TikTok
        3. Перейти на /upload
        4. Выбрать файл
        5. Заполнить описание
        6. Опубликовать
    
    Returns:
        JsonResponse: результат загрузки
    """
    pass  # TODO: Implement
```

### Следующие шаги

1. **Реализация авторизации:**
   - Создайте модуль `tiktok_auth.py`
   - Используйте Playwright для взаимодействия с TikTok
   - Обработка 2FA, CAPTCHA, email verification

2. **Реализация загрузки:**
   - Создайте модуль `tiktok_upload.py`
   - Селекторы для элементов страницы загрузки
   - Обработка процесса загрузки видео

3. **Интеграция Dolphin Anty:**
   - Создайте модуль `dolphin_client.py`
   - API клиент для Dolphin Anty
   - Управление профилями

4. **Worker для async задач:**
   - Настройте Celery
   - Создайте tasks.py с асинхронными задачами
   - Интегрируйте с views

## 📚 Ресурсы

- [TikTok Web Structure](https://www.tiktok.com) - для изучения селекторов
- [Dolphin Anty API](https://dolphin-anty.com/api) - документация API
- [Playwright Docs](https://playwright.dev/python/) - автоматизация браузера
- [Django Docs](https://docs.djangoproject.com/) - Django фреймворк

## 🤝 Контрибьюция

При реализации функций следуйте:
1. Используйте существующую документацию в функциях
2. Добавляйте подробные комментарии
3. Обрабатывайте все возможные ошибки
4. Логируйте все важные действия
5. Тестируйте на реальных аккаунтах

## 📄 Лицензия

Этот модуль является частью проекта Instagram Uploader и следует той же лицензии.


