# 🤖 Автоматическое решение reCAPTCHA v2

## Обзор

Этот проект теперь поддерживает автоматическое решение reCAPTCHA v2 через сервис [ruCAPTCHA](https://rucaptcha.com) во время загрузки в Instagram. Когда Instagram показывает капчу с текстом "Подтвердите, что это вы", система автоматически:

1. ✅ Обнаруживает reCAPTCHA iframe на странице
2. 🔍 Извлекает параметры капчи (sitekey, URL страницы)
3. 📤 Отправляет задачу в ruCAPTCHA API  
4. ⏳ Ожидает решения (10-120 секунд)
5. 💉 Автоматически вводит решение в страницу
6. ➡️ Нажимает кнопку "Далее" для продолжения

## 🛠 Настройка

### 1. Получите API ключ

1. Зарегистрируйтесь на [ruCAPTCHA.com](https://rucaptcha.com)
2. Пополните баланс (минимум $5 рекомендуется)
3. Получите API ключ в личном кабинете

### 2. Установите переменную окружения

**Вариант A: Через командную строку**
```bash
export RUCAPTCHA_API_KEY="your_api_key_here"
```

**Вариант B: Через .env файл**
```bash
echo "RUCAPTCHA_API_KEY=your_api_key_here" >> .env
```

**Вариант C: Альтернативное имя**
```bash
export CAPTCHA_API_KEY="your_api_key_here"
```

### 3. Проверьте конфигурацию

```bash
python manage.py check_captcha
```

Эта команда покажет:
- ✅ Статус подключения к API
- 💰 Текущий баланс
- ⚠️ Предупреждения о низком балансе
- 💡 Советы по настройке

### 4. Подробная проверка

```bash
python manage.py check_captcha --verbose
```

## 💰 Стоимость и баланс

- **reCAPTCHA v2**: ~$1 за 1000 решений
- **Время решения**: 10-120 секунд
- **Рекомендуемый минимальный баланс**: $5+

### Проверка баланса

```python
from uploader.captcha_solver import RuCaptchaSolver

solver = RuCaptchaSolver()
balance = solver.get_balance()
print(f"Баланс: ${balance}")
```

## 🔧 Как это работает

### Автоматическое обнаружение

Система автоматически обнаруживает reCAPTCHA по следующим признакам:

```python
# 1. iframe с reCAPTCHA
iframe[title*="recaptcha" i]
iframe[src*="recaptcha"]
iframe[id*="recaptcha"]
iframe[title*="Google Recaptcha"]

# 2. Скрытое поле для ответа
#g-recaptcha-response
#recaptcha-input
input[type="hidden"][id*="recaptcha"]

# 3. Текст на странице
"Подтвердите, что это вы"
"confirm that you are human"
```

### Извлечение sitekey

1. **data-sitekey атрибут**: `[data-sitekey]`
2. **iframe src**: `/[?&]k=([^&]+)/`
3. **JavaScript**: `window.grecaptcha`
4. **Известные ключи Instagram**: Автоматический fallback

### Процесс решения

```python
# 1. Создание задачи
task_data = {
    "type": "RecaptchaV2TaskProxyless",  # или RecaptchaV2Task с прокси
    "websiteURL": "https://www.instagram.com/...",
    "websiteKey": "6LfI9gcTAAAAAJz0P5ALAU4K4-kCpB9PBKH9q3Zu",
    "userAgent": "Mozilla/5.0...",
    "cookies": "session=abc123; csrf=xyz789"
}

# 2. Ожидание решения
solution = solver.solve_recaptcha_v2(site_key, page_url, proxy, user_agent, cookies)

# 3. Инъекция решения
document.querySelector('#g-recaptcha-response').value = solution;
```

## 📝 Логирование

Все действия логируются с префиксами:

- `🤖` - Запуск решения капчи
- `🔍` - Обнаружение капчи
- `📤` - Отправка задачи в API
- `⏳` - Ожидание решения
- `✅` - Успешное решение
- `💉` - Инъекция решения в страницу
- `❌` - Ошибки

Пример логов:
```
[2024-01-15 10:30:15] INFO 🤖 Starting reCAPTCHA v2 solving for https://www.instagram.com/...
[2024-01-15 10:30:16] INFO 🔍 reCAPTCHA iframe detected
[2024-01-15 10:30:16] INFO ✅ Found sitekey via data-sitekey: 6LfI9gcTAAAAAJ...
[2024-01-15 10:30:17] INFO 📤 Sending task to ruCAPTCHA: RecaptchaV2TaskProxyless
[2024-01-15 10:30:17] INFO ✅ Task created successfully. Task ID: 12345
[2024-01-15 10:30:22] INFO ⏳ Still processing... (5s elapsed)
[2024-01-15 10:30:35] INFO ✅ Captcha solved successfully!
[2024-01-15 10:30:35] INFO 💉 Injecting reCAPTCHA solution into page
[2024-01-15 10:30:37] INFO ✅ Captcha solved - Next button is now enabled
```

## 🔄 Интеграция с bulk upload

### Автоматические проверки

1. **Перед логином**: Проверка капчи на странице входа
2. **После логина**: Проверка постлогиновой капчи
3. **При верификации**: Специальная обработка "Подтвердите, что это вы"

### Обработка ошибок

- **Нет API ключа**: Продолжение без решения капчи
- **Низкий баланс**: Предупреждение, но попытка решения
- **Таймаут решения**: Повтор до 3 раз
- **Неудачная инъекция**: Повтор с разными методами

## ⚙️ Расширенная настройка

### Использование прокси

Система автоматически использует прокси аккаунта:

```python
proxy = {
    "type": "http",           # http, socks4, socks5
    "host": "1.2.3.4",
    "port": 8080,
    "login": "username",      # опционально
    "password": "password"    # опционально
}
```

### Настройка таймаутов

```python
solution = solver.solve_recaptcha_v2(
    site_key=site_key,
    page_url=page_url,
    timeout=180  # 3 минуты (по умолчанию 120)
)
```

### Кастомные User-Agent и куки

```python
user_agent = await page.evaluate('navigator.userAgent')
cookies = "; ".join([f"{c['name']}={c['value']}" for c in await page.context.cookies()])

solution = solver.solve_recaptcha_v2(
    site_key=site_key,
    page_url=page_url,
    user_agent=user_agent,
    cookies=cookies
)
```

## 🐛 Диагностика проблем

### Капча не обнаруживается

1. Проверьте логи на наличие:
   ```
   🔍 reCAPTCHA iframe detected
   ```

2. Если нет, возможно:
   - Капча загружается асинхронно (увеличьте ожидание)
   - Изменился селектор iframe
   - Instagram использует другой тип капчи

### Не удается найти sitekey

1. Проверьте логи:
   ```
   ✅ Found sitekey via data-sitekey: ...
   ```

2. Если "Could not find reCAPTCHA sitekey":
   - Используется fallback на известные ключи Instagram
   - Возможно изменился ключ (обновите в коде)

### Решение не принимается

1. Проверьте инъекцию:
   ```
   💉 Injecting reCAPTCHA solution into page
   ✅ Captcha solved - Next button is now enabled
   ```

2. Если кнопка не активируется:
   - Instagram изменил способ валидации
   - Нужно обновить селекторы кнопок
   - Проблема с callback функциями

### Низкая скорость решения

1. **Проверьте качество прокси**: Плохие прокси замедляют решение
2. **Время суток**: В пиковые часы ruCAPTCHA может быть медленнее
3. **Баланс**: При низком балансе приоритет может быть ниже

## 📚 API референс

### RuCaptchaSolver

```python
from uploader.captcha_solver import RuCaptchaSolver

# Создание экземпляра
solver = RuCaptchaSolver(api_key="your_key")

# Решение капчи
solution = solver.solve_recaptcha_v2(
    site_key="6LfI9gcTAAAAAJ...",
    page_url="https://www.instagram.com/accounts/login/",
    proxy={"type": "http", "host": "1.2.3.4", "port": 8080},
    user_agent="Mozilla/5.0...",
    cookies="session=abc123",
    timeout=120
)

# Проверка баланса
balance = solver.get_balance()
```

### Вспомогательные функции

```python
from uploader.captcha_solver import detect_recaptcha_on_page, solve_recaptcha_if_present

# Обнаружение капчи
captcha_params = detect_recaptcha_on_page(page)
# Возвращает: {"site_key": "...", "page_url": "...", "iframe_present": True}

# Автоматическое решение
success = await solve_recaptcha_if_present(page, account_details, max_attempts=3)
# Возвращает: True если решено или отсутствует, False если ошибка
```

## 🛡 Безопасность

- ✅ API ключ маскируется в логах
- ✅ Поддержка переменных окружения
- ✅ Graceful degradation (работа без ключа)
- ✅ Использование прокси аккаунта для анонимности

## 📞 Поддержка

Если возникают проблемы:

1. **Проверьте конфигурацию**: `python manage.py check_captcha --verbose`
2. **Изучите логи**: Ищите префиксы `🤖`, `🔍`, `❌`
3. **Проверьте баланс**: ruCAPTCHA должен иметь положительный баланс
4. **Обновите ключи**: Instagram может изменить sitekey

---

**💡 Совет**: Начните с небольшого баланса ($5-10) для тестирования, затем пополняйте по мере необходимости. 