# 🚀 Быстрый старт - обновленная форма создания аккаунта

## ✅ Что изменилось

1. ❌ **Удалено поле "Phone Number"**
2. ✅ **Добавлен импорт Cookies** (JSON текст или файл)

## 📋 Шаги для запуска

### 1. Применить миграцию базы данных

```bash
python manage.py makemigrations tiktok_uploader
```

Когда спросит про default для `created_at` - нажмите **Enter** (поле nullable).

```bash
python manage.py migrate tiktok_uploader
```

### 2. Перезапустить Django сервер

```bash
python manage.py runserver
```

### 3. Открыть форму создания аккаунта

Перейдите по адресу:
```
http://localhost:8000/tiktok/accounts/create/
```

## 🎯 Как использовать новые функции

### Создание аккаунта без cookies (как раньше)
1. Заполните Username, Password, Email
2. Выберите Proxy (опционально)
3. Отметьте "Create Dolphin Anty profile" (опционально)
4. Нажмите "Create Account"

### Создание аккаунта с cookies - Вариант 1 (JSON текст)
1. Заполните Username, Password, Email
2. **В поле "Cookies JSON"** вставьте cookies в формате JSON:
   ```json
   [
     {
       "name": "sessionid",
       "value": "your_value_here",
       "domain": ".tiktok.com",
       "path": "/",
       "secure": true,
       "httpOnly": true
     },
     {
       "name": "sid_tt",
       "value": "your_value_here",
       "domain": ".tiktok.com",
       "path": "/",
       "secure": true,
       "httpOnly": true
     }
   ]
   ```
3. Отметьте "Create Dolphin Anty profile"
4. Нажмите "Create Account"

### Создание аккаунта с cookies - Вариант 2 (загрузка файла)
1. Заполните Username, Password, Email
2. **Нажмите "Browse"** в поле "Or upload cookies file"
3. Выберите `.json` файл с cookies
4. Отметьте "Create Dolphin Anty profile"
5. Нажмите "Create Account"

## 📂 Пример файла cookies

См. файл `tiktok_uploader/static/cookies_example.json` для примера структуры.

## 🔧 Как получить cookies

### Способ 1: Chrome DevTools
1. Откройте TikTok в Chrome и войдите в аккаунт
2. Нажмите `F12`
3. Вкладка **Application** → **Cookies** → `https://www.tiktok.com`
4. Скопируйте нужные cookies

### Способ 2: Расширение EditThisCookie
1. Установите [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/)
2. Откройте TikTok и войдите
3. Кликните на иконку расширения
4. Нажмите **Export** → копируется JSON

### Способ 3: Cookie-Editor
1. Установите [Cookie-Editor](https://cookie-editor.cgagnier.ca/)
2. Откройте TikTok и войдите
3. Кликните на иконку → **Export** → **JSON**

## ✨ Что происходит с cookies

- ✅ **С Dolphin профилем**: Cookies импортируются автоматически в браузерный профиль
- ℹ️ **Без профиля**: Cookies сохраняются для последующего импорта
- ❌ **Ошибка формата**: Форма покажет ошибку валидации

## 📚 Подробная документация

- **COOKIES_IMPORT_GUIDE.md** - полное руководство по импорту cookies
- **ACCOUNT_FORM_UPDATE.md** - технические детали изменений

## ⚠️ Важные замечания

1. Cookies должны быть в формате **JSON массива** (не объекта!)
2. Обязательные поля: `name`, `value`, `domain`
3. Cookies содержат доступ к аккаунту - храните в безопасности
4. Для импорта cookies нужен **Dolphin профиль**
5. Phone number больше не требуется при создании аккаунта

## 🎉 Готово!

Теперь вы можете:
- ✅ Создавать аккаунты без phone_number
- ✅ Импортировать cookies двумя способами
- ✅ Автоматически загружать cookies в Dolphin
- ✅ Пропускать процесс авторизации для уже залогиненных аккаунтов

---

**Вопросы?** См. полную документацию в `COOKIES_IMPORT_GUIDE.md`




