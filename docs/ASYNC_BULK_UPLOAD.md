# ⚡ Асинхронная система загрузки

## 🚀 Обзор

Асинхронная версия bulk upload позволяет запускать **несколько аккаунтов параллельно** вместо последовательного выполнения, обеспечивая **3-5x ускорение** при работе с множественными аккаунтами.

### 🎯 Ключевые особенности
- **Параллельная обработка** - до 3 аккаунтов одновременно
- **Контроль ресурсов** - семафоры для предотвращения перегрузки
- **Асинхронные файлы** - эффективная работа с временными файлами
- **Real-time мониторинг** - live отслеживание прогресса
- **Graceful degradation** - плавное снижение нагрузки при проблемах

## ✨ Преимущества

- **Скорость**: 3-5x быстрее обычного режима
- **Параллельность**: до 3 аккаунтов одновременно  
- **Эффективность**: лучшее использование ресурсов
- **Мониторинг**: реальное время отслеживания прогресса
- **Стабильность**: автоматическое восстановление после сбоев
- **Масштабируемость**: легко настраиваемые параметры

## 🎯 Когда использовать

✅ **Используйте когда:**
- У вас 2+ аккаунта в задаче
- Система имеет достаточно ресурсов (8GB+ RAM)
- Стабильная сеть и прокси
- Нужна максимальная скорость обработки

❌ **НЕ используйте когда:**
- Только 1 аккаунт в задаче
- Ограниченные ресурсы системы (4GB RAM)
- Нестабильная сеть
- Требуется максимальная стабильность

## 🚀 Использование

### Через веб-интерфейс
```
http://localhost:8000/bulk-upload/start/123/?async=true
```

### Через CLI инструменты

#### Основные команды
```bash
# Список задач подходящих для async
python run_async_bulk_upload.py --list

# Запуск асинхронной загрузки
python run_async_bulk_upload.py --run-async 123

# Создание тестовой задачи
python run_async_bulk_upload.py --create

# Показать детальный статус/конфигурацию
python run_async_bulk_upload.py --config
```

#### Настройка параметров
```bash
# Для мощных систем (5 аккаунтов одновременно, быстрые задержки)
python run_async_bulk_upload.py --max-accounts 5 --account-delay-min 15

# Для обычных систем (2 аккаунта, консервативные задержки)
python run_async_bulk_upload.py --max-accounts 2 --account-delay-min 60

# Для стабильности (1 аккаунт, большие задержки)
python run_async_bulk_upload.py --max-accounts 1 --account-delay-min 120
```

#### Мониторинг и диагностика
```bash
# Проверить конфигурацию async
python run_async_bulk_upload.py --config

# Тест производительности без запуска браузеров
python run_async_bulk_upload.py --test-performance

# Очистка зависших процессов
python run_async_bulk_upload.py --cleanup
```

## ⚙️ Конфигурация
### Локализация (i18n)

- Каждая сессия формируется в соответствии с `InstagramAccount.locale` (например, `es_CL`, `pt_BR`).
- HTTP заголовок `Accept-Language` устанавливается на основе локали аккаунта и перекрывает настройки профиля Dolphin.
- Текстовые селекторы максимально языконезависимы; добавлены устойчивые испанские/португальские варианты для критичных кнопок (Log in/Next/Share/Not now и т.п.).


### Основные параметры
```python
# uploader/async_bulk_tasks.py - AsyncConfig
MAX_CONCURRENT_ACCOUNTS = 3    # Максимум аккаунтов одновременно
ACCOUNT_DELAY_MIN = 30         # Минимальная задержка между аккаунтами (сек)
ACCOUNT_DELAY_MAX = 120        # Максимальная задержка между аккаунтами (сек)
RETRY_ATTEMPTS = 2             # Количество попыток при ошибке
VIDEO_DELAY_MIN = 300          # Минимальная задержка между видео (сек)
VIDEO_DELAY_MAX = 900          # Максимальная задержка между видео (сек)
```

### Рекомендуемые настройки

#### Для высоконагруженных систем
```python
MAX_CONCURRENT_ACCOUNTS = 5
ACCOUNT_DELAY_MIN = 15
ACCOUNT_DELAY_MAX = 60
RETRY_ATTEMPTS = 3
```

#### Для стабильной работы
```python
MAX_CONCURRENT_ACCOUNTS = 2
ACCOUNT_DELAY_MIN = 60
ACCOUNT_DELAY_MAX = 180
RETRY_ATTEMPTS = 2
```

#### Для консервативного подхода
```python
MAX_CONCURRENT_ACCOUNTS = 1
ACCOUNT_DELAY_MIN = 120
ACCOUNT_DELAY_MAX = 300
RETRY_ATTEMPTS = 1
```

## 📈 Производительность

### Сравнение режимов

| Аккаунты/Видео | Синхронно | Асинхронно | Ускорение |
|----------------|-----------|------------|-----------|
| 3 акк × 1 видео | ~15 мин | ~5 мин | **3x** |
| 5 акк × 2 видео | ~45 мин | ~12 мин | **3.7x** |
| 10 акк × 1 видео | ~50 мин | ~15 мин | **3.3x** |

### Факторы влияния на производительность

#### Положительные факторы:
- ✅ **Больше аккаунтов** = больше параллелизма
- ✅ **Стабильные прокси** = меньше ошибок
- ✅ **SSD диски** = быстрее обработка файлов
- ✅ **Высокая RAM** = больше одновременных браузеров

#### Отрицательные факторы:
- ❌ **Нестабильная сеть** = больше таймаутов
- ❌ **Медленные прокси** = блокировка потоков
- ❌ **Instagram ограничения** = больше верификаций
- ❌ **Недостаток RAM** = swapping и замедление

## 🏗️ Архитектура

### Компоненты системы

#### AsyncTaskCoordinator
- **Управление параллельностью** через asyncio.Semaphore
- **Координация аккаунтов** - распределение задач
- **Мониторинг прогресса** - отслеживание статусов
- **Обработка результатов** - агрегация итогов

#### AsyncAccountProcessor
- **Обработка одного аккаунта** - полный цикл загрузки
- **Подготовка видео** - создание временных файлов
- **Запуск браузера** - через run_in_executor
- **Логирование** - детальные логи операций

#### AsyncWebLogger
- **Асинхронное логирование** - без блокировки event loop
- **Категоризация логов** - по типам операций
- **Цветовая кодировка** - для лучшей читаемости
- **Критические события** - сохранение в БД

### Поток данных
```
Task → Coordinator → Semaphore → Processors → Browsers → Results
```

## 🛠 Устранение проблем

### "Too many browsers"
```bash
# Уменьшить количество одновременных аккаунтов
python run_async_bulk_upload.py --max-accounts 2

# Увеличить задержки между аккаунтами
python run_async_bulk_upload.py --account-delay-min 120
```

### "Memory issues"  
```bash
# Уменьшить параллельность
python run_async_bulk_upload.py --max-accounts 1

# Увеличить задержки
python run_async_bulk_upload.py --account-delay-min 180

# Проверить использование памяти
python run_async_bulk_upload.py --monitor-resources
```

### "Network timeouts"
```bash
# Увеличить количество попыток
python run_async_bulk_upload.py --retry-attempts 3

# Увеличить таймауты
python run_async_bulk_upload.py --timeout 300

# Проверить качество прокси
python run_async_bulk_upload.py --test-proxies
```

### "Dolphin API errors"
```bash
# Проверить статус Dolphin
python -c "from bot.src.instagram_uploader.dolphin_anty import DolphinAnty; d = DolphinAnty('your-token'); print(d.check_dolphin_status())"

# Очистить зависшие профили
python run_async_bulk_upload.py --cleanup-dolphin
```

## 📊 Мониторинг

### Real-time статусы
- **PENDING** - задача ожидает запуска
- **RUNNING** - активная обработка
- **COMPLETED** - успешное завершение
- **FAILED** - критическая ошибка
- **PARTIALLY_COMPLETED** - частичный успех
- **PHONE_VERIFICATION_REQUIRED** - требуется верификация
- **HUMAN_VERIFICATION_REQUIRED** - требуется ручная проверка

### Метрики производительности
- **Время выполнения** - общее время задачи
- **Throughput** - аккаунтов в час
- **Success rate** - процент успешных загрузок
- **Error rate** - процент ошибок
- **Resource usage** - CPU, RAM, сеть

### Логи и диагностика
```bash
# Просмотр логов в реальном времени
tail -f logs/async_bulk_upload.log

# Поиск ошибок
grep "ERROR" logs/async_bulk_upload.log

# Анализ производительности
python run_async_bulk_upload.py --analyze-logs
```

## 💡 Рекомендации

### Для максимальной скорости
1. **Используйте 3-5 аккаунтов** одновременно
2. **Установите минимальные задержки** (15-30 сек)
3. **Используйте SSD диски** для файлов
4. **Обеспечьте стабильную сеть** и качественные прокси

### Для максимальной стабильности
1. **Ограничьте до 1-2 аккаунтов** одновременно
2. **Увеличьте задержки** (60-120 сек)
3. **Используйте надежные прокси**
4. **Мониторьте ресурсы** системы

### Общие рекомендации
1. **Тестируйте сначала на 2-3 аккаунтах**
2. **Мониторьте использование ресурсов**
3. **Используйте качественные прокси**
4. **Следите за лимитами Instagram**
5. **Регулярно очищайте временные файлы**
6. **Проверяйте логи на предмет ошибок**

## 🔧 Расширенная настройка

### Кастомные конфигурации
```python
# Создание кастомной конфигурации
from uploader.async_bulk_tasks import AsyncConfig

custom_config = AsyncConfig(
    max_concurrent_accounts=4,
    account_delay_min=45,
    account_delay_max=90,
    retry_attempts=3,
    timeout=600
)

# Использование в CLI
python run_async_bulk_upload.py --config-file custom_config.json
```

### Интеграция с мониторингом
```python
# Подключение внешних систем мониторинга
from uploader.async_bulk_tasks import AsyncTaskCoordinator

coordinator = AsyncTaskCoordinator(task_id, custom_config)
coordinator.add_monitoring_callback(custom_monitor_function)
```

---

Подробнее см. [README.md](README.md#асинхронная-загрузка) и [CHANGELOG.md](CHANGELOG.md) 