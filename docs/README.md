# Instagram Mass Uploader - Professional Automation Platform

🚀 **Профессиональная платформа для массовой загрузки видео в Instagram** с использованием Playwright и интеграции Dolphin Anty.

## 📋 Содержание

- [Обзор проекта](#обзор-проекта)
- [Архитектура системы](#архитектура-системы)
- [Основные возможности](#основные-возможности)
- [Установка и настройка](#установка-и-настройка)
- [Использование](#использование)
- [Конфигурация](#конфигурация)
- [API и интеграции](#api-и-интеграции)
- [Мониторинг и логирование](#мониторинг-и-логирование)
- [Устранение неполадок](#устранение-неполадок)
- [Разработка](#разработка)

## 🎯 Обзор проекта

Instagram Mass Uploader - это профессиональная платформа для автоматизации загрузки видео в Instagram с поддержкой множественных аккаунтов, прокси-серверов и человеческого поведения.

### Ключевые особенности

- **Многопользовательская архитектура** с поддержкой множественных аккаунтов
- **Асинхронная обработка** для повышения производительности
- **Интеграция с Dolphin Anty** для управления профилями браузера
- **Симуляция человеческого поведения** для обхода детекции
- **Поддержка 2FA** (Email, Authenticator)
- **Интеграция reCAPTCHA** для решения капчи
- **Прокси-поддержка** для каждого аккаунта
- **Мониторинг в реальном времени** и детальное логирование
- **Docker-контейнеризация** для простого развертывания
- **Оптимизация для Windows Server**

## 🏗️ Архитектура системы

### Технологический стек

```
Backend: Django + Celery
Browser Automation: Playwright + Dolphin Anty
Async Processing: asyncio + concurrent.futures
Database: SQLite/PostgreSQL
Frontend: Bootstrap + HTMX
Containerization: Docker + Docker Compose
```

### Структура проекта

```
instagram_uploader/
├── instagram_uploader/          # Django проект
│   ├── settings.py             # Настройки Django
│   ├── urls.py                 # URL маршруты
│   └── wsgi.py                 # WSGI конфигурация
├── uploader/                   # Основное приложение
│   ├── models.py               # Модели данных
│   ├── views.py                # Представления
│   ├── forms.py                # Формы
│   ├── admin.py                # Админ-панель
│   ├── constants.py            # Константы и селекторы
│   ├── human_behavior.py       # Симуляция человеческого поведения
│   ├── instagram_automation.py # Основная логика автоматизации
│   ├── bulk_tasks_playwright.py # Массовые задачи
│   ├── async_bulk_tasks.py     # Асинхронные задачи
│   ├── captcha_solver.py       # Решение капчи
│   ├── crop_handler.py         # Обработка обрезки видео
│   └── browser_utils.py        # Утилиты браузера
├── bot/                        # Автономный бот
│   └── src/instagram_uploader/
│       ├── dolphin_anty.py     # Интеграция с Dolphin
│       ├── upload_playwright.py # Загрузка через Playwright
│       ├── auth_playwright.py  # Аутентификация
│       └── browser_dolphin.py  # Работа с браузером
├── docs/                       # Документация
├── media/                      # Медиа файлы
├── prepared_videos/            # Подготовленные видео
└── requirements.txt            # Зависимости Python
```

### Модели данных

#### Основные модели

1. **InstagramAccount** - Аккаунты Instagram
   - Поля: username, password, email_username, email_password, tfa_secret
   - Статусы: ACTIVE, BLOCKED, LIMITED, INACTIVE, PHONE_VERIFICATION_REQUIRED
   - Связи: proxy, dolphin_profile_id

2. **Proxy** - Прокси-серверы
   - Типы: HTTP, SOCKS5, HTTPS
   - Статусы: active, inactive, banned, checking
   - Поля: host, port, username, password, country, city

3. **BulkUploadTask** - Массовые задачи загрузки
   - Статусы: PENDING, RUNNING, COMPLETED, FAILED, PARTIALLY_COMPLETED
   - Поля: name, status, log, upload_id, default_location, default_mentions

4. **BulkUploadAccount** - Аккаунты в массовой задаче
   - Связи: bulk_task, account, proxy
   - Статусы: PENDING, RUNNING, COMPLETED, FAILED

5. **BulkVideo** - Видео для массовой загрузки
   - Поля: video_file, location, mentions, order
   - Связи: bulk_task, assigned_to

## 🚀 Основные возможности

### 1. Массовая загрузка видео

- **Поддержка множественных аккаунтов** в одной задаче
- **Автоматическое распределение** видео между аккаунтами
- **Настройка задержек** между загрузками
- **Обработка ошибок** и повторные попытки
- **Мониторинг прогресса** в реальном времени

### 2. Асинхронная обработка

- **Параллельная обработка** аккаунтов (3-5x быстрее)
- **Настраиваемое количество** одновременных аккаунтов
- **Адаптивные задержки** между аккаунтами
- **Управление ресурсами** системы

### 3. Интеграция с Dolphin Anty

- **Автоматическое создание** профилей браузера
- **Синхронизация удаления** профилей при удалении аккаунтов
- **Обновление прокси** в профилях
- **Очистка зависших** профилей

### 4. Симуляция человеческого поведения

- **Случайные задержки** между действиями
- **Реалистичные движения** мыши
- **Естественные паттерны** прокрутки
- **Моделирование усталости** аккаунта
- **Осведомленность о времени** суток

### 5. Обработка верификации

- **Email верификация** с автоматическим получением кодов
- **2FA поддержка** (Authenticator, SMS)
- **Человеческая верификация** с ожиданием
- **reCAPTCHA решение** через API

### 6. Управление прокси

- **Автоматическое назначение** прокси аккаунтам
- **Проверка работоспособности** прокси
- **Ротация прокси** при блокировках
- **Географическое распределение**

## 💻 Установка и настройка

### Системные требования

- **Python 3.8+**
- **Docker Desktop** (для контейнеризации)
- **Dolphin Anty** (для управления профилями)
- **8GB+ RAM** (для асинхронной обработки)
- **SSD накопитель** (для быстрой работы с видео)

### Быстрый старт (Windows Server)

#### 1. Клонирование репозитория

```bash
git clone https://github.com/YOUR_USERNAME/instagram-mass-uploader.git
cd instagram-mass-uploader
```

#### 2. Настройка окружения

```bash
# Копирование шаблона окружения
copy windows_deployment.env.example windows_deployment.env

# Редактирование конфигурации
notepad windows_deployment.env
```

**Критические настройки для Windows:**
```env
# ВАЖНО: Для Docker на Windows используйте host.docker.internal
DOLPHIN_API_HOST=http://host.docker.internal:3001
DOLPHIN_API_TOKEN=your-dolphin-api-token

# Настройки сервера
ALLOWED_HOSTS=localhost,127.0.0.1,YOUR_WINDOWS_SERVER_IP
SECRET_KEY=your-super-secret-key-change-this

# Опционально: reCAPTCHA решение
RUCAPTCHA_API_KEY=your-rucaptcha-api-key
```

#### 3. Развертывание с Docker

```bash
# Сборка и запуск сервисов
docker-compose -f docker-compose.windows.yml up -d

# Просмотр логов
docker-compose -f docker-compose.windows.yml logs -f
```

#### 4. Доступ к панели управления

Откройте браузер: `http://YOUR_SERVER_IP:8000`

### Ручная установка

#### 1. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 3. Настройка базы данных

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Запуск сервера

```bash
python manage.py runserver 0.0.0.0:8000
```

## 📖 Использование

### Веб-интерфейс

#### 1. Создание массовой задачи

1. Перейдите в раздел "Массовые загрузки"
2. Нажмите "Создать новую задачу"
3. Заполните:
   - **Название задачи**
   - **Выберите аккаунты** для загрузки
   - **Загрузите видео** (поддерживаются форматы: MP4, MOV, AVI)
   - **Настройте локации** и упоминания (опционально)

#### 2. Настройка параметров

- **Задержки между видео**: 3-7 минут
- **Задержки между аккаунтами**: 30-120 секунд
- **Максимум видео на аккаунт**: 50
- **Повторные попытки**: 3 раза

#### 3. Запуск задачи

- **Синхронный режим**: Последовательная обработка
- **Асинхронный режим**: Параллельная обработка (рекомендуется)

### CLI инструменты

#### Массовая загрузка

```bash
# Список всех задач
python run_bulk_upload.py --list

# Создание тестовой задачи
python run_bulk_upload.py --create

# Запуск задачи
python run_bulk_upload.py --run 5

# Детальный статус
python run_bulk_upload.py --status 5
```

#### Асинхронная массовая загрузка

```bash
# Список подходящих задач
python run_async_bulk_upload.py --list

# Создание асинхронной тестовой задачи
python run_async_bulk_upload.py --create

# Запуск асинхронной задачи
python run_async_bulk_upload.py --run-async 5

# Сравнение производительности
python run_async_bulk_upload.py --compare 5

# Настройка параметров
python run_async_bulk_upload.py --max-accounts 3 --account-delay-min 30
```

### Управление аккаунтами

#### Добавление аккаунта

1. Перейдите в "Аккаунты Instagram"
2. Нажмите "Добавить аккаунт"
3. Заполните:
   - **Username** и **Password**
   - **Email** и **Email Password** (для 2FA)
   - **TFA Secret** (если используется Authenticator)
   - **Proxy** (опционально)

#### Настройка прокси

1. Перейдите в "Прокси"
2. Нажмите "Добавить прокси"
3. Заполните:
   - **Host** и **Port**
   - **Username** и **Password** (если требуется)
   - **Тип прокси**: HTTP, SOCKS5, HTTPS
   - **Страна** и **Город** (для геотаргетинга)

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию | Обязательная |
|------------|----------|---------------|--------------|
| `DOLPHIN_API_TOKEN` | Токен API Dolphin Anty | - | ✅ |
| `DOLPHIN_API_HOST` | Хост API Dolphin | `http://localhost:3001/v1.0` | ❌ |
| `RUCAPTCHA_API_KEY` | API ключ для решения reCAPTCHA | - | ❌ |
| `SECRET_KEY` | Секретный ключ Django | - | ✅ |
| `ALLOWED_HOSTS` | Разрешенные хосты Django | `localhost,127.0.0.1` | ❌ |
| `DEBUG` | Режим отладки | `True` | ❌ |
| `DATABASE_PATH` | Путь к базе данных | `db.sqlite3` | ❌ |

### Асинхронная конфигурация

| Настройка | Описание | По умолчанию | Диапазон |
|-----------|----------|---------------|----------|
| `MAX_CONCURRENT_ACCOUNTS` | Максимум одновременных аккаунтов | 3 | 1-5 |
| `ACCOUNT_DELAY_MIN` | Минимальная задержка между аккаунтами (сек) | 30 | 10-300 |
| `ACCOUNT_DELAY_MAX` | Максимальная задержка между аккаунтами (сек) | 120 | 30-600 |
| `RETRY_ATTEMPTS` | Количество повторных попыток | 2 | 1-5 |

### Временные константы

```python
# Задержки между действиями
HUMAN_DELAY_MIN = 0.5  # секунды
HUMAN_DELAY_MAX = 2.0  # секунды

# Задержки между аккаунтами
ACCOUNT_DELAY_MIN = 30   # секунды
ACCOUNT_DELAY_MAX = 120  # секунды

# Задержки между видео
VIDEO_DELAY_MIN = 180  # 3 минуты
VIDEO_DELAY_MAX = 420  # 7 минут

# Задержки между батчами
BATCH_PROCESSING_DELAY_MIN = 300   # 5 минут
BATCH_PROCESSING_DELAY_MAX = 900   # 15 минут
```

## 🔌 API и интеграции

### Dolphin Anty API

#### Основные методы

```python
from bot.src.instagram_uploader.dolphin_anty import DolphinAnty

# Инициализация
dolphin = DolphinAnty(api_token)

# Проверка статуса
status = dolphin.check_dolphin_status()

# Создание профиля
profile = dolphin.create_profile(account_data)

# Удаление профиля
dolphin.delete_profile(profile_id)

# Обновление прокси
dolphin.update_profile_proxy(profile_id, proxy_data)
```

#### Управление профилями

- **Автоматическое создание** профилей для новых аккаунтов
- **Синхронизация удаления** при удалении аккаунтов
- **Обновление прокси** в профилях
- **Очистка зависших** профилей

### reCAPTCHA API

#### Интеграция с RuCaptcha

```python
from uploader.captcha_solver import CaptchaSolver

solver = CaptchaSolver(api_key)

# Решение reCAPTCHA
solution = solver.solve_recaptcha(site_key, page_url)

# Решение hCaptcha
solution = solver.solve_hcaptcha(site_key, page_url)
```

### Email API

#### Получение кодов верификации

```python
from bot.src.instagram_uploader.email_client import EmailClient

client = EmailClient(email_config)

# Получение кода из email
code = client.get_verification_code()
```

## 📊 Мониторинг и логирование

### Система логирования

#### Уровни логирования

- **INFO**: Обычные операции
- **WARNING**: Некритичные проблемы
- **ERROR**: Критические ошибки
- **DEBUG**: Детальная отладочная информация

#### Категории логов

- `TASK_INFO`: Управление задачами
- `ACCOUNT_PROCESS`: Обработка аккаунтов
- `BROWSER`: Операции браузера
- `VERIFICATION`: Обработка верификации
- `DOLPHIN`: Операции с Dolphin API

### Мониторинг в реальном времени

#### Метрики производительности

- **Время выполнения** задач
- **Количество успешных** загрузок
- **Процент ошибок** по аккаунтам
- **Использование ресурсов** системы

#### Алерты

- **Блокировка аккаунтов** Instagram
- **Проблемы с прокси**
- **Ошибки Dolphin API**
- **Превышение лимитов** загрузок

### Логи и отчеты

#### Структура логов

```
logs/
├── task_123.log          # Логи конкретной задачи
├── account_username.log   # Логи аккаунта
├── dolphin_api.log       # Логи Dolphin API
├── browser_operations.log # Логи браузера
└── system.log           # Системные логи
```

#### Анализ логов

```bash
# Поиск ошибок
grep "ERROR" logs/task_*.log

# Анализ производительности
grep "COMPLETED" logs/task_*.log | wc -l

# Проверка блокировок
grep "BLOCKED\|SUSPENDED" logs/account_*.log
```

## 🔧 Устранение неполадок

### Частые проблемы

#### 1. Проблемы с Dolphin API

```bash
# Проверка статуса Dolphin
python -c "from bot.src.instagram_uploader.dolphin_anty import DolphinAnty; d = DolphinAnty('your-token'); print(d.check_dolphin_status())"
```

**Решения:**
- Проверьте, что Dolphin Anty запущен
- Убедитесь в правильности API токена
- Проверьте настройки сети и файрвола

#### 2. Проблемы с асинхронной загрузкой

```bash
# Тест производительности
python run_async_bulk_upload.py --compare <task_id>

# Проверка конфигурации
python run_async_bulk_upload.py --config
```

**Решения:**
- Уменьшите количество одновременных аккаунтов
- Увеличьте задержки между аккаунтами
- Проверьте доступность ресурсов системы

#### 3. Очистка зависших процессов

```bash
# Принудительная очистка процессов браузера
python manage.py shell -c "from uploader.browser_support import cleanup_hanging_browser_processes; cleanup_hanging_browser_processes()"
```

#### 4. Проблемы с верификацией

**Email верификация:**
- Проверьте настройки email клиента
- Убедитесь в правильности email/password
- Проверьте доступность IMAP/SMTP серверов

**2FA верификация:**
- Проверьте правильность TFA secret
- Убедитесь в синхронизации времени
- Проверьте настройки Authenticator приложения

### Оптимизация производительности

#### Для высоконагруженных загрузок

1. **Увеличьте количество одновременных аккаунтов**: `--max-accounts 5`
2. **Уменьшите задержки**: `--account-delay-min 15`
3. **Используйте SSD** для хранения видео файлов
4. **Оптимизируйте настройки прокси**

#### Для стабильности

1. **Уменьшите количество одновременных аккаунтов**: `--max-accounts 2`
2. **Увеличьте задержки**: `--account-delay-min 60`
3. **Мониторьте ресурсы** системы
4. **Используйте надежные прокси**

### Диагностика проблем

#### Проверка системы

```bash
# Проверка окружения
python check_env.py

# Диагностика прокси
python uploader/proxy_diagnostics.py

# Проверка уникальности видео
python uniq_video.py
```

#### Анализ производительности

```bash
# Сравнение синхронного и асинхронного режимов
python run_async_bulk_upload.py --compare <task_id>

# Анализ логов производительности
grep "PERFORMANCE" logs/*.log
```

## 🛠️ Разработка

### Структура кода

#### Основные модули

1. **uploader/models.py** - Модели данных Django
2. **uploader/views.py** - Представления веб-интерфейса
3. **uploader/instagram_automation.py** - Основная логика автоматизации
4. **uploader/human_behavior.py** - Симуляция человеческого поведения
5. **uploader/constants.py** - Константы и селекторы
6. **bot/src/instagram_uploader/dolphin_anty.py** - Интеграция с Dolphin

#### Принципы разработки

- **SOLID принципы** - Четкое разделение ответственности
- **DRY** - Избежание дублирования кода
- **KISS** - Простота и читаемость
- **Модульность** - Независимые компоненты

### Добавление новых функций

#### 1. Создание новой модели

```python
# uploader/models.py
class NewFeature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "New Feature"
        verbose_name_plural = "New Features"
```

#### 2. Добавление представления

```python
# uploader/views.py
from django.shortcuts import render
from .models import NewFeature

def new_feature_view(request):
    features = NewFeature.objects.all()
    return render(request, 'uploader/new_feature.html', {
        'features': features
    })
```

#### 3. Настройка URL

```python
# uploader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('new-feature/', views.new_feature_view, name='new_feature'),
]
```

### Тестирование

#### Запуск тестов

```bash
# Запуск всех тестов
python manage.py test

# Запуск конкретного теста
python manage.py test uploader.tests.TestUploader

# Запуск с покрытием
coverage run --source='.' manage.py test
coverage report
```

#### Создание тестов

```python
# uploader/tests.py
from django.test import TestCase
from .models import InstagramAccount

class InstagramAccountTest(TestCase):
    def setUp(self):
        self.account = InstagramAccount.objects.create(
            username='test_user',
            password='test_pass'
        )
    
    def test_account_creation(self):
        self.assertEqual(self.account.username, 'test_user')
        self.assertEqual(self.account.status, 'ACTIVE')
```

### Развертывание

#### Docker развертывание

```bash
# Сборка образа
docker build -f Dockerfile.windows -t instagram-uploader .

# Запуск контейнера
docker run -d -p 8000:8000 --name instagram-app instagram-uploader

# Просмотр логов
docker logs instagram-app
```

#### PowerShell автоматизация

```powershell
# Запуск скрипта развертывания
.\deploy_windows.ps1
```

## 📚 Дополнительная документация

- [Руководство по разработке](DEVELOPMENT.md)
- [Развертывание на Windows](WINDOWS_DEPLOYMENT.md)
- [Асинхронная массовая загрузка](ASYNC_BULK_UPLOAD.md)
- [Устранение неполадок](TROUBLESHOOTING.md)
- [Настройка reCAPTCHA](RECAPTCHA_SETUP.md)
- [Документация Dolphin API](Dolphin{anty}%20Remote%20API%20-%20Detailed%20Python%20Documentation.md)

## 🤝 Поддержка

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/instagram-mass-uploader/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/instagram-mass-uploader/discussions)
- **Documentation**: [Wiki](https://github.com/YOUR_USERNAME/instagram-mass-uploader/wiki)

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## ⚠️ Отказ от ответственности

Этот инструмент предназначен для образовательных целей. Пожалуйста, соблюдайте Условия использования Instagram и используйте ответственно.

---

**Версия документации**: 2.0  
**Последнее обновление**: 2024  
**Автор**: Instagram Mass Uploader Team 