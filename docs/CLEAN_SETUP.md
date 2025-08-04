# 🧹 Чистая настройка Instagram Uploader

## Что мы исправили
- ❌ Удалили 16 лишних `.cmd` файлов
- ❌ Убрали проблемный маппинг `staticfiles` из docker-compose
- ❌ Упростили Dockerfile 
- ✅ Оставили одну простую команду для запуска

## Инструкция для Windows

### 1. Получить изменения
```cmd
git pull
```

### 2. Запустить чистую пересборку
```cmd
rebuild_clean.cmd
```

**Всё!** Один файл делает всё:
- Останавливает контейнеры
- Очищает Docker кеш
- Пересобирает образ
- Запускает приложение
- Тестирует статические файлы

### 3. Результат
- 🌐 Приложение: http://localhost:8000
- 🔐 Логин: `admin` / `admin123`
- 📋 Логи: `docker-compose -f docker-compose.windows.simple.yml logs -f`

## Что изменилось

### Было (проблемы):
- 16+ различных `.cmd` файлов
- Маппинг `./staticfiles:/app/staticfiles` создавал конфликты
- Сложный Dockerfile с множеством проверок
- Дублирование статических файлов

### Стало (просто):
- 1 файл `rebuild_clean.cmd` 
- Статические файлы создаются только внутри контейнера
- Простой Dockerfile
- Никаких дубликатов

## Если что-то не работает

Посмотрите логи:
```cmd
docker-compose -f docker-compose.windows.simple.yml logs -f
```

Статические файлы должны отдаваться с кодом 200:
- CSS: http://localhost:8000/static/css/apple-style.css
- JS: http://localhost:8000/static/js/apple-ui.js
- Logo: http://localhost:8000/static/css/logo.svg 