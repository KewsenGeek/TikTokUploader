# 🔄 Функция перезапуска задач прогрева

**Дата:** 2025-10-05  
**Статус:** ✅ Реализовано

---

## 📋 Описание

Добавлена возможность **перезапуска задач прогрева** (Warmup Tasks), которые завершились со статусом `FAILED` или `COMPLETED`.

### **Зачем это нужно?**

1. ✅ **Повторная попытка при ошибках** - если задача прогрева упала из-за временных проблем (сеть, прокси, TikTok), можно попробовать еще раз
2. ✅ **Дополнительный прогрев** - можно запустить прогрев повторно для тех же аккаунтов
3. ✅ **Экономия времени** - не нужно создавать новую задачу с теми же настройками

---

## 🎯 Функциональность

### **Кнопка "Restart Task"**

Появляется на странице детализации задачи прогрева (`/tiktok/warmup/<task_id>/`) только для задач со статусом:
- ✅ **COMPLETED** - задача успешно завершена
- ✅ **FAILED** - задача завершилась с ошибкой

### **Что происходит при рестарте?**

1. **Сброс статуса задачи:**
   - `status` → `PENDING`
   - `started_at` → `None`
   - `completed_at` → `None`

2. **Сброс статусов всех аккаунтов в задаче:**
   - `status` → `PENDING`
   - `started_at` → `None`
   - `completed_at` → `None`
   - В лог добавляется запись: `========== TASK RESTARTED ==========`

3. **После рестарта:**
   - Появляется кнопка **"Start Warmup"**
   - Можно запустить задачу заново

---

## 💻 Реализация

### 1. **View: `restart_warmup_task` в `views_warmup.py`**

```python
@login_required
def restart_warmup_task(request, task_id):
    """
    Перезапуск задачи прогрева.
    Сбрасывает статусы и позволяет запустить задачу заново.
    """
    if request.method != 'POST':
        messages.error(request, 'Invalid request method')
        return redirect('tiktok_uploader:warmup_task_detail', task_id=task_id)
    
    try:
        task = get_object_or_404(WarmupTask, id=task_id)
        
        # Проверяем что задача не в процессе выполнения
        if task.status == 'RUNNING':
            messages.error(request, 'Cannot restart a task that is currently running.')
            return redirect('tiktok_uploader:warmup_task_detail', task_id=task_id)
        
        # Сбрасываем статус задачи
        task.status = 'PENDING'
        task.started_at = None
        task.completed_at = None
        task.save(update_fields=['status', 'started_at', 'completed_at'])
        
        # Сбрасываем статусы всех аккаунтов
        for warmup_account in task.accounts.all():
            warmup_account.status = 'PENDING'
            warmup_account.started_at = None
            warmup_account.completed_at = None
            # Добавляем запись о рестарте в лог
            warmup_account.log += f"\n[{timezone.now()}] ========== TASK RESTARTED ==========\n"
            warmup_account.save()
        
        logger.info(f"Warmup task {task_id} ({task.name}) restarted by user")
        messages.success(request, f'Warmup task "{task.name}" has been reset. You can now start it again.')
        
    except Exception as e:
        logger.error(f"Error restarting warmup task {task_id}: {str(e)}")
        messages.error(request, f'Error restarting task: {str(e)}')
    
    return redirect('tiktok_uploader:warmup_task_detail', task_id=task_id)
```

---

### 2. **URL в `urls.py`**

```python
path('warmup/<int:task_id>/restart/', views_warmup.restart_warmup_task, name='restart_warmup_task'),
```

---

### 3. **Кнопка в шаблоне `detail.html`**

```html
{% if task.status == 'COMPLETED' or task.status == 'FAILED' %}
    <form method="post" action="{% url 'tiktok_uploader:restart_warmup_task' task.id %}" style="display:inline;">
        {% csrf_token %}
        <button type="submit" class="btn btn-warning btn-lg" 
                onclick="return confirm('Restart this warmup task? All progress will be reset.')">
            <i class="bi bi-arrow-clockwise"></i> Restart Task
        </button>
    </form>
{% endif %}
```

---

## 🎨 UI/UX

### **Визуальное отображение:**

#### **До рестарта (задача FAILED):**
```
╔════════════════════════════════════════════════╗
║  🔥 Warmup Task #5                             ║
║  [FAILED]  Created: 2025-10-05 18:46          ║
║                                                ║
║  [🔄 Restart Task]  [🗑️ Delete]               ║
╚════════════════════════════════════════════════╝
```

#### **После рестарта (задача PENDING):**
```
╔════════════════════════════════════════════════╗
║  🔥 Warmup Task #5                             ║
║  [PENDING]  Created: 2025-10-05 18:46         ║
║                                                ║
║  [▶️ Start Warmup]  [🗑️ Delete]               ║
╚════════════════════════════════════════════════╝
```

---

### **Confirmation Dialog:**

При нажатии на **"Restart Task"** появляется подтверждение:

```
⚠️ Are you sure?

Restart this warmup task? 
All progress will be reset.

[Cancel]  [OK]
```

---

### **Success Message:**

После успешного рестарта:

```
✅ Warmup task "Warmup 2025-10-05 18:46" has been reset. 
   You can now start it again.
```

---

## 📊 Лог аккаунта при рестарте

В логах каждого аккаунта появляется разделитель:

```
[2025-10-05 18:46:52] Started warming up account
[2025-10-05 18:46:55] Authentication failed
[2025-10-05 18:46:55] ========== TASK RESTARTED ==========
[2025-10-05 18:50:00] Started warming up account
[2025-10-05 18:50:15] Warmup completed successfully
```

Это помогает отследить повторные попытки в истории выполнения задачи.

---

## 🔒 Ограничения

### **Нельзя перезапустить задачу в статусе RUNNING:**

```python
if task.status == 'RUNNING':
    messages.error(request, 'Cannot restart a task that is currently running.')
    return redirect('tiktok_uploader:warmup_task_detail', task_id=task_id)
```

**Сообщение:**
```
❌ Cannot restart a task that is currently running.
```

---

## 🧪 Тестирование

### **Сценарий 1: Рестарт задачи с ошибкой**

1. Создайте задачу прогрева с аккаунтами
2. Запустите задачу
3. Дождитесь статуса `FAILED` (или искусственно установите его)
4. Перейдите на страницу детализации задачи
5. Нажмите **"Restart Task"**
6. Подтвердите действие
7. ✅ Задача сбросится в статус `PENDING`
8. ✅ Появится кнопка **"Start Warmup"**

---

### **Сценарий 2: Рестарт успешно завершенной задачи**

1. Создайте задачу прогрева
2. Запустите и дождитесь статуса `COMPLETED`
3. Нажмите **"Restart Task"**
4. Подтвердите действие
5. ✅ Задача сбросится и можно запустить снова

---

### **Сценарий 3: Попытка рестарта работающей задачи**

1. Создайте и запустите задачу (статус `RUNNING`)
2. Попытайтесь нажать **"Restart Task"** (кнопка не отображается)
3. ✅ Кнопка не доступна для работающих задач

---

## 📈 Преимущества

### 1. **Удобство:**
- ✅ Не нужно создавать новую задачу с теми же настройками
- ✅ История выполнения сохраняется в логах
- ✅ Быстрый доступ к повторному запуску

### 2. **Экономия времени:**
- ✅ Один клик вместо заполнения формы создания задачи
- ✅ Все аккаунты и настройки уже выбраны

### 3. **Отладка:**
- ✅ Можно повторить задачу после исправления проблем (прокси, Dolphin профили)
- ✅ Логи показывают все попытки выполнения

---

## 🔗 Связанные документы

- `WARMUP_COMPLETE.md` - Полная документация Warmup Tasks
- `PLAYWRIGHT_ASYNC_CONTEXT_FIX.md` - Исправление ошибок async контекста
- `TIKTOK_BULK_IMPORT_COMPLETE.md` - Документация импорта аккаунтов

---

## 📝 Changelog

### **2025-10-05:**
- ✅ Добавлена функция `restart_warmup_task` в `views_warmup.py`
- ✅ Добавлен URL `/warmup/<task_id>/restart/`
- ✅ Добавлена кнопка "Restart Task" в `detail.html`
- ✅ Добавлены проверки и error handling
- ✅ Добавлены логи для отслеживания рестартов

---

## ✅ Статус: РЕАЛИЗОВАНО

Функция перезапуска задач прогрева полностью реализована и готова к использованию! 🎉

**Попробуйте прямо сейчас:**
1. Перейдите к любой завершенной задаче прогрева
2. Нажмите **"Restart Task"**
3. Запустите задачу заново!

