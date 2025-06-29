# 🔧 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### 1. Database Connection Error: "unable to open database file"

**Симптомы:**
```
sqlite3.OperationalError: unable to open database file
django.db.utils.OperationalError: unable to open database file
```

**Причина:** Проблемы с правами доступа к SQLite файлу на Windows в Docker.

**Решение:**
```cmd
# Полная очистка и перезапуск
restart_clean.cmd
```

**Объяснение:** Windows Docker имеет проблемы с монтированием SQLite файлов как volumes. Новая версия создает базу данных внутри контейнера в Docker volume.

---

### 2. Static Files Not Loading (CSS, JS, Logo missing)

**Симптомы:**
- Логотип не отображается
- CSS стили не применяются (сайт выглядит без стилей)
- JavaScript не работает
- 404 ошибки для `/static/css/apple-style.css`, `/static/js/apple-ui.js`, `/static/css/logo.svg`

**Причина:** Статические файлы не копируются в правильное место при сборке Docker образа.

**Быстрое решение:**
```cmd
# Быстрое исправление статических файлов
fix_static_files.cmd
```

**Полное решение:**
```cmd
# Полная пересборка с исправлением
restart_clean.cmd
```

**Объяснение:** Django ищет статические файлы в `STATICFILES_DIRS`, но они были только в `uploader/static/`. Исправление добавляет корректные пути.

---

### 3. Server Error 500 on /cookies/ page

**Симптомы:**
```
TemplateDoesNotExist: uploader/cookies/dashboard.html
django.template.exceptions.TemplateDoesNotExist
```

**Причина:** Отсутствует темплейт для страницы cookies (уже исправлено в новой версии).

**Решение:**
```cmd
# Обновите контейнер
restart_clean.cmd
```

---

### 4. Container Won't Start

**Симптомы:**
- Container exits immediately
- No logs in `docker-compose logs`

**Диагностика:**
```cmd
check_status.cmd
```

**Решения:**
```cmd
# 1. Проверьте доступность портов
netstat -an | findstr :8000

# 2. Остановите все контейнеры
docker stop $(docker ps -q)

# 3. Полная очистка
restart_clean.cmd
```

---

### 5. Cannot Access Dolphin Anty API

**Симптомы:**
- "Connection refused" errors
- Browser profiles not loading

**Проверка:**
```cmd
# Проверьте что Dolphin Anty запущен на порту 3001
curl http://localhost:3001/v1.0/browser_profiles
```

**Решение:** Убедитесь что:
1. ✅ Dolphin Anty Local API Server запущен
2. ✅ Порт 3001 доступен  
3. ✅ В `.env` файле: `DOLPHIN_API_HOST=http://host.docker.internal:3001`

---

### 6. Memory/Performance Issues

**Симптомы:**
- Slow performance
- Container crashes with OOM

**Решение:**
```yaml
# В docker-compose.windows.simple.yml увеличьте лимиты:
deploy:
  resources:
    limits:
      memory: 4G    # Увеличьте с 2G
      cpus: '2'     # Увеличьте с 1
```

---

## 🔍 Диагностические команды

### Проверить статус системы:
```cmd
check_status.cmd
```

### Быстрое исправление статических файлов:
```cmd
fix_static_files.cmd
```

### Посмотреть логи:
```cmd
docker-compose -f docker-compose.windows.simple.yml logs -f
```

### Войти в контейнер:
```cmd
docker-compose -f docker-compose.windows.simple.yml exec web bash
```

### Проверить статические файлы в контейнере:
```cmd
docker-compose -f docker-compose.windows.simple.yml exec web ls -la /app/staticfiles/css/
```

### Проверить базу данных:
```cmd
docker-compose -f docker-compose.windows.simple.yml exec web python manage.py shell
```
```python
from django.contrib.auth import get_user_model
User = get_user_model()
print(f"Users count: {User.objects.count()}")
```

---

## 📊 Monitoring & Logs

### Местонахождение логов:
- **Application logs:** `./logs/`
- **Django logs:** В контейнере `/app/django.log`
- **Docker logs:** `docker-compose logs`

### Мониторинг ресурсов:
```cmd
# CPU и память контейнера
docker stats

# Место на диске
docker system df
```

---

## 🆘 Emergency Reset

Если ничего не работает:

```cmd
# 1. Остановить все
docker-compose -f docker-compose.windows.simple.yml down
docker stop $(docker ps -q)

# 2. Очистить все
docker system prune -af
docker volume prune -f

# 3. Полный перезапуск
restart_clean.cmd
```

⚠️ **Внимание:** Это удалит ВСЕ данные (аккаунты, загруженные медиа, логи)

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/ssuvorin/instagram-mass-uploader-windows/issues)
- 📧 Email: support@example.com
- 💬 Telegram: @your_telegram 