# 13. Керування портами розробки

## 🚨 ОБОВ'ЯЗКОВЕ ПРАВИЛО: Централізоване керування портами

### КРИТИЧНО: Перед запуском будь-якого dev server

**ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ ДІЙ:**

#### 1️⃣ Перевірка реєстру портів

**ЗАВЖДИ** перед запуском dev server перевір реєстр:

```python
from common.port_manager import PortManager

# Отримати порти проекту
ports = PortManager.get_project_ports("projectflow")
print(f"Виділені порти: {ports}")
# {"web": 3000, "api": 3001}

# Перевірити доступність порту
is_free, project = PortManager.check_port_available(3000)
if not is_free:
    print(f"[ERROR] Порт 3000 зайнятий проектом {project}")
    exit(1)

# Знайти наступний вільний порт (якщо потрібно)
free_port = PortManager.get_next_available_port(start_port=3000)
print(f"Вільний порт: {free_port}")
```

#### 2️⃣ Запуск ЛИШЕ на виділеному порту

**✅ ПРАВИЛЬНО:**
```bash
# Next.js web application
npm run dev -- -p 3000

# FastAPI backend
uvicorn main:app --port 8000 --reload

# Vite frontend
npm run dev -- --port 3005
```

**❌ НЕПРАВИЛЬНО:**
```bash
# Випадковий порт - може зайняти чужий!
npm run dev

# Невірний порт - конфлікт з іншим проектом
npm run dev -- -p 3010
```

#### 3️⃣ ЗАБОРОНЕНО УБИВАТИ ВСІ СЕРВЕРИ

**❌ КАТЕГОРИЧНО ЗАБОРОНЕНО:**
```bash
# ЦЕ УБИВАЄ ВСІ Node.js ПРОЦЕСИ В СИСТЕМІ!
taskkill /f /im node.exe  # ❌ ЗАБОРОНЕНО

# ЦЕ УБИВАЄ ВСІ Python ПРОЦЕСИ!
taskkill /f /im python.exe  # ❌ ЗАБОРОНЕНО
```

**✅ ПРАВИЛЬНО - завершення конкретного порту:**
```bash
# Завершити ТІЛЬКИ конкретний порт
npx kill-port 3000

# Завершити кілька конкретних портів
npx kill-port 3000 3001 8000

# Альтернатива для Windows (знайти PID та завершити)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

#### 4️⃣ Приклад правильного workflow

```python
from common.port_manager import PortManager
import subprocess
import sys

def start_dev_server(project_name: str, service_name: str):
    """
    Запустити dev server з перевіркою портів.

    Args:
        project_name: Назва проекту з реєстру
        service_name: Назва сервісу (web, api, etc.)
    """
    # Крок 1: Отримати виділений порт
    ports = PortManager.get_project_ports(project_name)
    if not ports or service_name not in ports:
        print(f"[ERROR] Порт для {project_name}/{service_name} не знайдено в реєстрі")
        sys.exit(1)

    port = ports[service_name]
    print(f"[INFO] Виділений порт для {project_name}/{service_name}: {port}")

    # Крок 2: Перевірити доступність
    is_free, occupied_by = PortManager.check_port_available(port)
    if not is_free:
        print(f"[ERROR] Порт {port} зайнятий проектом {occupied_by}")
        print(f"[INFO] Використовуйте: npx kill-port {port}")
        sys.exit(1)

    # Крок 3: Запустити на виділеному порті
    print(f"[OK] Запуск dev server на порті {port}...")
    subprocess.run(["npm", "run", "dev", "--", "-p", str(port)])

# Використання:
start_dev_server("projectflow", "web")
```

## 📋 РЕЄСТР ПОРТІВ

**Файл:** `D:\Automation\PROJECT_PORTS_REGISTRY.json`

**Структура:**
- `projects` - всі проекти з виділеними портами
- `reserved_ports` - діапазони для різних типів сервісів
- `port_allocation_rules` - правила розподілу портів

**Утиліта:** `D:\Automation\common\port_manager.py`

### Доступні методи PortManager:

| Метод | Опис | Приклад |
|-------|------|---------|
| `get_project_ports(name)` | Отримати порти проекту | `ports = PortManager.get_project_ports("projectflow")` |
| `check_port_available(port)` | Перевірити занятість в реєстрі | `is_free, proj = PortManager.check_port_available(3000)` |
| `is_port_open_on_system(port)` | Перевірити реальне системне стан | `is_open = PortManager.is_port_open_on_system(3000)` |
| `get_next_available_port(start, end)` | Знайти вільний порт | `free = PortManager.get_next_available_port(3000, 3020)` |
| `update_project_ports(name, ports)` | Оновити порти проекту | `PortManager.update_project_ports("myproj", {"web": 3011})` |
| `validate_registry()` | Перевірити на конфлікти | `is_valid, errors = PortManager.validate_registry()` |
| `list_all_projects()` | Список всіх проектів | `projects = PortManager.list_all_projects()` |
| `get_project_info(name)` | Повна інформація про проект | `info = PortManager.get_project_info("projectflow")` |

## ⚠️ ЧОМУ ЦЕ КРИТИЧНО

### Проблеми без централізованого керування портами:

1. **Конфлікти портів** - два проекти на одному порті
2. **Перевантаження системи** - багато dev серверів на випадкових портах
3. **Зупинка всієї розробки** - `taskkill /f /im node.exe` убиває ВСІ проекти
4. **Паралельна розробка неможлива** - конфлікти між проектами

### Переваги централізованого керування:

1. ✅ Кожен проект на виділених портах
2. ✅ Паралельна розробка без конфліктів
3. ✅ Завершення конкретних портів без впливу на інші
4. ✅ Прозорість - завжди відомо хто займає який порт

## 🔍 ВАЛІДАЦІЯ РЕЄСТРУ

**Перевірка на конфлікти:**

```python
from common.port_manager import PortManager

# Валідувати реєстр портів
is_valid, errors = PortManager.validate_registry()

if not is_valid:
    print("[ERROR] Знайдено конфлікти портів:")
    for error in errors:
        print(f"  - {error}")
else:
    print("[OK] Реєстр портів валідний")
```

**Виведення стану всіх проектів:**

```python
from common.port_manager import PortManager

projects = PortManager.list_all_projects()
for name, data in projects.items():
    print(f"\n{name}:")
    print(f"  Шлях: {data.get('local_path', 'N/A')}")
    print(f"  Порти: {data.get('ports', {})}")
    print(f"  Технології: {', '.join(data.get('tech_stack', []))}")
```

## 📚 РОЗШИРЕНІ СЦЕНАРІЇ ВИКОРИСТАННЯ

### Сценарій 1: Автоматичний пошук вільного порту

```python
from common.port_manager import PortManager

# Знайти вільний порт в діапазоні web applications
free_port = PortManager.get_next_available_port(3000, 3020)
print(f"Використовуйте порт: {free_port}")

# Додати новий проект з знайденим портом
PortManager.update_project_ports(
    "new-project",
    {"web": free_port},
    create_if_not_exists=True
)
```

### Сценарій 2: Перевірка перед запуском

```python
from common.port_manager import PortManager
import sys

project = "patternshift"
service = "web"

# Перевірка 1: Порт виділений в реєстрі?
ports = PortManager.get_project_ports(project)
if service not in ports:
    print(f"[ERROR] Сервіс {service} не знайдено для {project}")
    sys.exit(1)

port = ports[service]

# Перевірка 2: Порт вільний в реєстрі?
is_available, occupied = PortManager.check_port_available(port)
if not is_available:
    print(f"[ERROR] Порт {port} зайнятий: {occupied}")
    sys.exit(1)

# Перевірка 3: Порт вільний в системі?
is_open = PortManager.is_port_open_on_system(port)
if not is_open:
    print(f"[WARNING] Порт {port} зайнятий в системі (не в реєстрі)")
    print(f"[INFO] Завершіть процес: npx kill-port {port}")
    sys.exit(1)

print(f"[OK] Порт {port} готовий до використання")
```

### Сценарій 3: Очищення зайнятих портів

```python
from common.port_manager import PortManager
import subprocess

project = "projectflow"

# Отримати всі порти проекту
ports = PortManager.get_project_ports(project)

for service, port in ports.items():
    if port is None:
        continue

    # Перевірити чи зайнятий порт
    is_open = PortManager.is_port_open_on_system(port)
    if not is_open:
        print(f"[INFO] Завершення процесу на порті {port} ({service})...")
        subprocess.run(["npx", "kill-port", str(port)])
    else:
        print(f"[OK] Порт {port} ({service}) вільний")
```

## 🎯 КОЛИ ЧИТАТИ ЦЕЙ МОДУЛЬ

**ОБОВ'ЯЗКОВО ПРОЧИТАТИ:**
- Перед запуском будь-якого dev server
- При створенні нового проекту з портами
- При виникненні конфліктів портів
- Коли потрібно завершити dev server

**ПОСИЛАННЯ:**
- Реєстр портів: `D:\Automation\PROJECT_PORTS_REGISTRY.json`
- Утиліта: `D:\Automation\common\port_manager.py`
- CLI приклади: `python -m common.port_manager`

---

**Версія:** 1.0
**Дата створення:** 2025-10-12
**Автор:** Archon Implementation Engineer
