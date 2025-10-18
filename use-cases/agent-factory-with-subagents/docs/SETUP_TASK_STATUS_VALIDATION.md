# Установка автоматичної валідації статусів задач Archon

**Дата створення:** 2025-10-18
**Версія:** 1.0
**Автор:** Blueprint Architect

---

## 📋 Огляд

Цей документ описує процес установки автоматичної валідації статусів задач Archon перед git коммітами.

**Мета:** Автоматично блокувати коммі якщо задача має неправильний статус:
- ❌ Блокує коміт якщо статус "todo" (робота не почата)
- ❌ Блокує коміт якщо статус "doing" (робота не завершена)
- ✅ Дозволяє коміт якщо статус "done" або "review"

**Graceful Degradation:** Якщо Archon MCP Server недоступний - пропускає перевірку з warning.

---

## ✅ Передумови

### Необхідне програмне забезпечення:

1. **Python 3.7+**
   ```bash
   python --version  # Повинно бути >= 3.7
   ```

2. **Git Repository**
   ```bash
   git status  # Повинно працювати без помилок
   ```

3. **Archon MCP Server** (опціонально, але рекомендовано)
   - Працює на `localhost:3000`
   - Якщо недоступний - валідація пропускається з warning

---

## 🔧 Установка

### Варіант 1: Автоматична установка (РЕКОМЕНДОВАНО)

#### Linux / macOS:

```bash
# 1. Перейти в кореневу директорію проекту
cd /path/to/agent-factory/use-cases/agent-factory-with-subagents

# 2. Запустити скрипт установки
python common/install_task_status_validation.py

# 3. Перевірити установку
ls -la .git/hooks/commit-msg
```

#### Windows (PowerShell):

```powershell
# 1. Перейти в кореневу директорію проекту
cd D:\Automation\agent-factory\use-cases\agent-factory-with-subagents

# 2. Запустити скрипт установки
python common/install_task_status_validation.py

# 3. Перевірити установку
dir .git\hooks\commit-msg
```

---

### Варіант 2: Ручна установка

#### Linux / macOS:

```bash
# 1. Створити файл хука
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh
#
# Archon Task Status Validation Hook
# Автоматично перевіряє статус задачі перед комітом
#

SCRIPT_PATH="common/validate_task_status_before_commit.py"

# Перевірка наявності Python
if ! command -v python3 &> /dev/null; then
    echo "[WARNING] Python3 not found - skipping validation"
    exit 0
fi

# Перевірка наявності скрипта валідації
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[WARNING] Validation script not found at $SCRIPT_PATH - skipping validation"
    exit 0
fi

# Запуск валідації
python3 "$SCRIPT_PATH" "$1"
exit $?
EOF

# 2. Зробити хук виконуваним
chmod +x .git/hooks/commit-msg

# 3. Перевірити установку
ls -la .git/hooks/commit-msg
```

#### Windows (Git Bash):

```bash
# 1. Створити файл хука
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh
#
# Archon Task Status Validation Hook
# Автоматично перевіряє статус задачі перед комітом
#

SCRIPT_PATH="common/validate_task_status_before_commit.py"

# Перевірка наявності Python
if ! command -v python &> /dev/null; then
    echo "[WARNING] Python not found - skipping validation"
    exit 0
fi

# Перевірка наявності скрипта валідації
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[WARNING] Validation script not found at $SCRIPT_PATH - skipping validation"
    exit 0
fi

# Запуск валідації
python "$SCRIPT_PATH" "$1"
exit $?
EOF

# 2. Зробити хук виконуваним (Git Bash автоматично робить це на Windows)
chmod +x .git/hooks/commit-msg

# 3. Перевірити установку
ls -la .git/hooks/commit-msg
```

#### Windows (PowerShell - альтернативний метод):

```powershell
# 1. Створити файл хука
$hookContent = @'
#!/bin/sh
#
# Archon Task Status Validation Hook
# Автоматично перевіряє статус задачі перед комітом
#

SCRIPT_PATH="common/validate_task_status_before_commit.py"

# Перевірка наявності Python
if ! command -v python &> /dev/null; then
    echo "[WARNING] Python not found - skipping validation"
    exit 0
fi

# Перевірка наявності скрипта валідації
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "[WARNING] Validation script not found at $SCRIPT_PATH - skipping validation"
    exit 0
fi

# Запуск валідації
python "$SCRIPT_PATH" "$1"
exit $?
'@

# 2. Записати вміст в файл
$hookContent | Out-File -FilePath .git\hooks\commit-msg -Encoding ASCII

# 3. Перевірити установку
Get-ChildItem .git\hooks\commit-msg
```

---

## 🧪 Тестування установки

### Тест 1: Перевірка що хук запускається

```bash
# Створити тестовий коміт
echo "test" > test.txt
git add test.txt
git commit -m "Test commit without Task ID"

# Очікуваний результат:
# [OK] No Task ID found in commit message - skipping validation
```

### Тест 2: Перевірка валідації з Task ID

```bash
# Створити коміт з Task ID (замініть на реальний ID з Archon)
git commit -m "[TASK_ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349] Test task validation"

# Очікуваний результат (якщо статус "todo" або "doing"):
# [ERROR] COMMIT BLOCKED - Task status is 'todo'
# (детальне повідомлення з інструкціями)
```

### Тест 3: Перевірка graceful degradation

```bash
# Зупинити Archon MCP Server
# Потім створити коміт з Task ID

git commit -m "[TASK_ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349] Test graceful degradation"

# Очікуваний результат:
# [WARNING] Error connecting to Archon MCP: ...
# [WARNING] Skipping validation (graceful degradation)
# [коміт дозволено]
```

---

## 📝 Формати Task ID в повідомленнях коммітів

Валідація підтримує наступні формати Task ID:

### Формат 1: З квадратними дужками (РЕКОМЕНДОВАНО)
```
[TASK_ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349] Implement new feature
```

### Формат 2: Без дужок
```
Task ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349
Implement new feature
```

### Формат 3: Нижній регістр
```
task_id: e7cb2e05-21fe-450e-af2c-25ac1b6b8349
Implement new feature
```

**Примітка:** Task ID повинен бути валідним UUID формату `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

---

## 🚨 Вирішення проблем

### Проблема 1: Хук не запускається

**Симптоми:**
- Коміт проходить без жодних повідомлень про валідацію

**Рішення:**
```bash
# Перевірити що хук існує
ls -la .git/hooks/commit-msg

# Перевірити що хук виконуваний (Linux/macOS)
chmod +x .git/hooks/commit-msg

# Перевірити вміст хука
cat .git/hooks/commit-msg
```

### Проблема 2: Python not found

**Симптоми:**
```
[WARNING] Python not found - skipping validation
```

**Рішення:**
```bash
# Встановити Python 3.7+
# Linux: sudo apt install python3
# macOS: brew install python3
# Windows: завантажити з python.org

# Перевірити установку
python3 --version  # Linux/macOS
python --version   # Windows
```

### Проблема 3: Validation script not found

**Симптоми:**
```
[WARNING] Validation script not found at common/validate_task_status_before_commit.py
```

**Рішення:**
```bash
# Перевірити що скрипт існує
ls -la common/validate_task_status_before_commit.py

# Якщо файл відсутній - скопіювати з репозиторію або створити знову
```

### Проблема 4: Archon MCP Server connection refused

**Симптоми:**
```
[WARNING] Error connecting to Archon MCP: Connection refused
[WARNING] Skipping validation (graceful degradation)
```

**Рішення:**
```bash
# Перевірити що Archon MCP Server запущений
curl http://localhost:3000/health

# Якщо не запущений - запустити сервер
cd /path/to/archon-mcp-server
npm start
```

### Проблема 5: Task not found in Archon

**Симптоми:**
```
[WARNING] Task e7cb2e05-... not found in Archon
[WARNING] Skipping validation (graceful degradation)
```

**Рішення:**
- Перевірити що Task ID в повідомленні коміту правильний
- Перевірити що задача існує в Archon MCP Server
- Використати правильний формат Task ID (UUID)

---

## 🔓 Обхід валідації (тільки для екстрених випадків)

### Варіант 1: Тимчасово вимкнути хук

```bash
# Перейменувати хук (Linux/macOS/Git Bash)
mv .git/hooks/commit-msg .git/hooks/commit-msg.disabled

# Зробити коміт
git commit -m "Emergency fix"

# Відновити хук
mv .git/hooks/commit-msg.disabled .git/hooks/commit-msg
```

### Варіант 2: Використати --no-verify

```bash
# Пропустити всі хуки (включаючи валідацію)
git commit --no-verify -m "Emergency fix without validation"
```

**⚠️ УВАГА:** Використовуйте обхід валідації ТІЛЬКИ в критичних ситуаціях!
Після екстреного коміту:
1. Оновіть статус задачі вручну
2. Створіть ретроспективну задачу для аналізу ситуації
3. Задокументуйте причину обходу валідації

---

## 🔗 Інтеграція з існуючими git workflows

### Співпраця з іншими хуками

Якщо у вас вже є `commit-msg` хук:

```bash
# 1. Зберегти існуючий хук
mv .git/hooks/commit-msg .git/hooks/commit-msg.old

# 2. Створити новий хук який викликає обидва
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh

# Викликати старий хук
if [ -f .git/hooks/commit-msg.old ]; then
    .git/hooks/commit-msg.old "$1"
    OLD_EXIT=$?
    if [ $OLD_EXIT -ne 0 ]; then
        exit $OLD_EXIT
    fi
fi

# Викликати валідацію Archon
SCRIPT_PATH="common/validate_task_status_before_commit.py"
if [ -f "$SCRIPT_PATH" ] && command -v python3 &> /dev/null; then
    python3 "$SCRIPT_PATH" "$1"
    exit $?
fi

exit 0
EOF

# 3. Зробити виконуваним
chmod +x .git/hooks/commit-msg
```

### Використання з Husky

Якщо проект використовує Husky для git hooks:

```json
// package.json
{
  "husky": {
    "hooks": {
      "commit-msg": "python3 common/validate_task_status_before_commit.py $HUSKY_GIT_PARAMS"
    }
  }
}
```

---

## 📊 Статистика та моніторинг

### Переглянути всі заблоковані комміти

```bash
# Перегляньте git reflog для заблокованих спроб
git reflog
```

### Автоматичні звіти (майбутнє покращення)

Планується додати:
- Логування всіх перевірок валідації
- Статистика блокування коммітів
- Інтеграція з системою моніторингу Archon

---

## 🔄 Оновлення валідаційного скрипта

```bash
# 1. Отримати останню версію з репозиторію
git pull origin main

# 2. Перевірити що скрипт оновлений
python3 common/validate_task_status_before_commit.py --version

# 3. Хук автоматично використовує нову версію
```

---

## 📚 Додаткові ресурси

### Документація:
- [02_workflow_rules.md](../.claude/rules/02_workflow_rules.md) - ЧЕРВОНІ ЛІНІЇ для оновлення статусів
- [03_task_management.md](../.claude/rules/03_task_management.md) - Обов'язкова структура TodoWrite
- [10_post_task_checklist.md](../.claude/rules/10_post_task_checklist.md) - Post-Task Checklist з оновленням статусу

### Зв'язок з системою захисту:
Цей хук реалізує **Рівень 3** системи захисту:
- **Рівень 1:** Обов'язкові пункти TodoWrite
- **Рівень 2:** ЧЕРВОНІ ЛІНІЇ в правилах workflow
- **Рівень 3:** Автоматична валідація (ЦЕЙ ХУК!)

---

## ✅ Checklist установки

- [ ] Python 3.7+ встановлено
- [ ] Git repository ініціалізовано
- [ ] Archon MCP Server працює (опціонально)
- [ ] Хук створено в `.git/hooks/commit-msg`
- [ ] Хук зроблено виконуваним (Linux/macOS)
- [ ] Тест без Task ID пройшов
- [ ] Тест з Task ID пройшов
- [ ] Тест graceful degradation пройшов
- [ ] Документація прочитана
- [ ] Команда поінформована про нові правила

---

**Версія:** 1.0
**Останнє оновлення:** 2025-10-18
**Контакт:** Blueprint Architect
**Статус:** ✅ Production Ready
