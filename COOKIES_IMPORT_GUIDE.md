# 🍪 Руководство по импорту Cookies

## Обзор

Вы можете импортировать cookies в TikTok аккаунт двумя способами:
1. **Вставить JSON** напрямую в текстовое поле
2. **Загрузить файл** с cookies в формате JSON

## 📋 Формат Cookies

Cookies должны быть в виде JSON массива объектов. Каждый объект представляет одну cookie:

```json
[
  {
    "name": "sessionid",
    "value": "ваше_значение_здесь",
    "domain": ".tiktok.com",
    "path": "/",
    "secure": true,
    "httpOnly": true
  },
  {
    "name": "sid_tt",
    "value": "ваше_значение_здесь",
    "domain": ".tiktok.com",
    "path": "/",
    "secure": true,
    "httpOnly": true
  }
]
```

### Обязательные поля:
- `name` - название cookie
- `value` - значение cookie
- `domain` - домен (обычно `.tiktok.com`)

### Необязательные поля:
- `path` - путь (по умолчанию `/`)
- `secure` - флаг HTTPS (по умолчанию `true`)
- `httpOnly` - флаг HTTP-only (по умолчанию `false`)
- `sameSite` - политика SameSite (`Strict`, `Lax`, `None`)
- `expirationDate` - дата истечения (timestamp)

## 🔧 Как получить cookies

### Способ 1: Из браузера (Chrome)

1. Откройте TikTok и войдите в аккаунт
2. Нажмите F12 для открытия DevTools
3. Перейдите на вкладку **Application**
4. В левом меню выберите **Cookies** → `https://www.tiktok.com`
5. Скопируйте нужные cookies

### Способ 2: Расширение EditThisCookie

1. Установите расширение [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/) для Chrome
2. Откройте TikTok и войдите в аккаунт
3. Нажмите на иконку расширения
4. Нажмите кнопку **Export** (экспорт)
5. Cookies скопируются в буфер обмена в формате JSON

### Способ 3: Расширение Cookie-Editor

1. Установите [Cookie-Editor](https://cookie-editor.cgagnier.ca/)
2. Откройте TikTok и войдите в аккаунт
3. Нажмите на иконку расширения
4. Нажмите **Export** → **JSON**
5. Скопируйте или сохраните в файл

## 📝 Использование в интерфейсе

### Создание нового аккаунта

1. Перейдите в **Accounts** → **Create New**
2. Заполните основные данные (username, password, email)
3. В секции **Cookies (Optional)**:
   - **Вариант А**: Вставьте JSON в текстовое поле "Cookies JSON"
   - **Вариант Б**: Нажмите "Browse" и загрузите файл `.json`
4. Отметьте "Create Dolphin Anty profile automatically" если нужно
5. Нажмите **Create Account**

### Что происходит:

- Если **Dolphin профиль создается** → cookies импортируются автоматически в профиль
- Если **профиль уже существует** → cookies импортируются в существующий профиль
- Если **профиль не создается** → cookies сохраняются для последующего использования

## ✅ Важные cookies для TikTok

Основные cookies, необходимые для авторизации:

- `sessionid` - основная сессия
- `sid_tt` - TikTok session ID
- `sid_guard` - защита сессии
- `uid_tt` - user ID
- `ttwid` - TikTok web ID
- `passport_csrf_token` - CSRF токен
- `csrf_session_id` - session CSRF

## 🔍 Пример файла cookies

См. файл `tiktok_uploader/static/cookies_example.json` для примера структуры.

## ❌ Типичные ошибки

### 1. Неверный формат JSON
```
❌ НЕПРАВИЛЬНО:
{name: "sessionid", value: "123"}

✅ ПРАВИЛЬНО:
[{"name": "sessionid", "value": "123", "domain": ".tiktok.com"}]
```

### 2. Не массив, а объект
```
❌ НЕПРАВИЛЬНО:
{"sessionid": "123", "sid_tt": "456"}

✅ ПРАВИЛЬНО:
[
  {"name": "sessionid", "value": "123", "domain": ".tiktok.com"},
  {"name": "sid_tt", "value": "456", "domain": ".tiktok.com"}
]
```

### 3. Отсутствие domain
```
❌ НЕПРАВИЛЬНО:
[{"name": "sessionid", "value": "123"}]

✅ ПРАВИЛЬНО:
[{"name": "sessionid", "value": "123", "domain": ".tiktok.com"}]
```

## 🛠 Устранение неполадок

### "Invalid JSON format"
- Проверьте, что JSON валиден (используйте https://jsonlint.com/)
- Убедитесь, что используете двойные кавычки `"`, а не одинарные `'`
- Проверьте, что все скобки закрыты

### "Cookies import failed"
- Убедитесь, что Dolphin Anty запущен
- Проверьте, что профиль существует
- Убедитесь, что формат cookies правильный

### "Account created but cookies not imported"
- Cookies сохранены, но профиль не был создан
- Создайте профиль вручную или отметьте checkbox при создании

## 🎯 Советы

1. **Экспортируйте все cookies** - лучше больше, чем меньше
2. **Используйте свежие cookies** - чем новее, тем лучше
3. **Проверяйте срок действия** - некоторые cookies могут истечь
4. **Храните в безопасности** - cookies = доступ к аккаунту
5. **Используйте один браузер** - не смешивайте cookies из разных источников

## 📚 Дополнительно

- После импорта cookies проверьте работу через **Cookie Robot**
- Для обновления cookies используйте тот же процесс
- Cookies автоматически обновляются после успешного входа

---

**Примечание**: Cookies содержат конфиденциальную информацию. Никогда не делитесь ими и храните в безопасном месте.




