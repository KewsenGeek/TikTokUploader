# 🚀 Быстрый старт: Массовый импорт TikTok аккаунтов

## 📝 Подготовка файла

Создайте текстовый файл (например, `accounts.txt`) с аккаунтами:

```
username1:password123
username2:password456:user2@email.com:emailpass
username3:password789:user3@gmail.com:emailpass123
```

**Формат:** `username:password[:email[:email_password]]`

---

## 🔥 Импорт в 3 клика

### 1️⃣ Откройте страницу импорта
```
TikTok Accounts → Import
```
или прямая ссылка: `http://localhost:8000/tiktok/accounts/import/`

### 2️⃣ Заполните форму
- **File**: Выберите ваш `accounts.txt`
- **Locale**: `English (United States)` ✅
- **Proxy**: `Match Locale` (автоматически подберет US прокси) ✅
- **Profiles**: `Create Dolphin Profiles` ✅
- **Client**: Опционально

### 3️⃣ Нажмите "Start Import"

**Готово!** ✅ 

Аккаунты импортированы, прокси назначены, Dolphin профили созданы!

---

## 📊 Что произошло?

```
✅ Successfully created 3 new account(s).
🐬 Created 3 Dolphin profile(s).
```

Для каждого аккаунта:
- ✅ Создана запись в БД
- ✅ Назначен прокси из US
- ✅ Создан Dolphin профиль с прокси
- ✅ Аккаунт готов к прогреву и загрузке!

---

## ⚡ Важные моменты

### Прокси
- **1 аккаунт = 1 прокси** (автоматически)
- Убедитесь что есть достаточно прокси: `TikTok Proxies → Import`

### Dolphin Anty
- Должен быть запущен
- `DOLPHIN_API_TOKEN` настроен в `.env`

### Формат файла
- ✅ UTF-8 encoding
- ✅ Один аккаунт на строку
- ✅ Пустые строки пропускаются
- ✅ Строки с `#` игнорируются (комментарии)

---

## 🎯 Готово к работе!

После импорта можете:
- 🔥 **Создать Warmup Task** → Прогрев аккаунтов
- 📹 **Создать Bulk Upload** → Массовая загрузка видео
- 👥 **Создать Follow Task** → Подписки/отписки

**Следующий шаг:** Warmup Tasks (Прогрев) →


