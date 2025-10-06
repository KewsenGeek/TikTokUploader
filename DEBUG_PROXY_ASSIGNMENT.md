# 🔍 Отладка назначения прокси

## ✅ Что исправлено

### 1. Синхронизация proxy и current_proxy
**Было:**
```python
if account.proxy:
    account.current_proxy = account.proxy
```

**Стало:**
```python
account.current_proxy = account.proxy  # Всегда синхронизируем!
```

Теперь `current_proxy` синхронизируется независимо от значения `proxy` (включая `None`).

### 2. Добавлены отладочные логи
```python
print(f"[EDIT ACCOUNT DEBUG] Selected proxy ID from form: {selected_proxy_id}")
print(f"[EDIT ACCOUNT DEBUG] After form save - proxy: {account.proxy}, current_proxy: {account.current_proxy}")
print(f"[EDIT ACCOUNT DEBUG] After account.save() - proxy: {account.proxy}, current_proxy: {account.current_proxy}")
```

---

## 🧪 Как протестировать

### Шаг 1: Откройте терминал с запущенным сервером
Если сервер не запущен:
```bash
.venv\Scripts\python.exe manage.py runserver
```

### Шаг 2: Откройте редактирование аккаунта
```
http://localhost:8000/tiktok/accounts/1/edit/
```

### Шаг 3: Выберите прокси и сохраните
1. В секции "Proxy Settings" выберите прокси из списка
2. Нажмите "Save Changes"
3. **СРАЗУ СМОТРИТЕ В КОНСОЛЬ СЕРВЕРА!**

### Шаг 4: Проверьте вывод в консоли
Вы должны увидеть что-то вроде:
```
[EDIT ACCOUNT DEBUG] Selected proxy ID from form: <TikTokProxy: 192.168.1.1:8080>
[EDIT ACCOUNT DEBUG] After form save - proxy: 192.168.1.1:8080, current_proxy: 192.168.1.1:8080
[EDIT ACCOUNT DEBUG] After account.save() - proxy: 192.168.1.1:8080, current_proxy: 192.168.1.1:8080
```

---

## 📋 Возможные проблемы и решения

### Проблема 1: Selected proxy ID = None
```
[EDIT ACCOUNT DEBUG] Selected proxy ID from form: None
```

**Причина:** Форма не передает значение прокси  
**Решение:** Проверьте что в форме есть поле `<select name="proxy">`

### Проблема 2: After form save - proxy: None
```
[EDIT ACCOUNT DEBUG] After form save - proxy: None, current_proxy: None
```

**Причина:** form.save() не сохраняет прокси  
**Решение:** Проверьте что 'proxy' есть в Meta.fields формы

### Проблема 3: Прокси сбрасывается после account.save()
```
[EDIT ACCOUNT DEBUG] After form save - proxy: 192.168.1.1:8080, current_proxy: 192.168.1.1:8080
[EDIT ACCOUNT DEBUG] After account.save() - proxy: None, current_proxy: None
```

**Причина:** Модель TikTokAccount имеет кастомный метод save()  
**Решение:** Проверьте метод save() в модели

---

## 🔍 Дополнительная проверка через shell

Проверьте что прокси действительно сохранился:
```bash
.venv\Scripts\python.exe manage.py shell
```

```python
from tiktok_uploader.models import TikTokAccount

acc = TikTokAccount.objects.get(id=1)
print(f"Username: {acc.username}")
print(f"Proxy: {acc.proxy}")
print(f"Current Proxy: {acc.current_proxy}")
```

---

## 📝 Что делать дальше

### Если логи показывают что прокси сохраняется:
✅ Проблема решена! Просто перезагрузите страницу.

### Если прокси все еще None:
1. Скопируйте вывод из консоли сервера
2. Покажите мне логи
3. Я увижу на каком этапе теряется прокси

---

## 🎯 Попробуйте сейчас!

1. Убедитесь что сервер запущен
2. Откройте http://localhost:8000/tiktok/accounts/1/edit/
3. Выберите прокси
4. Нажмите "Save Changes"
5. **СМОТРИТЕ В КОНСОЛЬ СЕРВЕРА!**
6. Скопируйте и покажите мне что выводится

---

**Файлы изменены:**
- `tiktok_uploader/views.py` - исправлена синхронизация, добавлены логи
- `tiktok_uploader/forms.py` - добавлен `__init__()` для queryset прокси


