# 09. Протокол аналізу проблем

## 🚨 КРАСНА ЛІНІЯ: НІ ОДНОГО РІШЕННЯ БЕЗ АНАЛІЗУ КОНТЕКСТУ

**Проблема:** Агенти пропонують рішення "наугад" без аналізу контексту, створюють ЩЕ БІЛЬШЕ помилок.

**Рішення:** Обов'язковий протокол аналізу ПЕРЕД кожним рішенням.

---

## 📋 ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ при проблемах

```
ЕТАП 0: ОТРИМАННЯ ПРОБЛЕМИ
└─ Користувач повідомляє про проблему/помилку

ЕТАП 1: АНАЛІЗ КОНТЕКСТУ (ОБОВ'ЯЗКОВО!)
├─ git log --oneline -20 → що робилось нещодавно
├─ git log --grep="ключові слова" → релевантні коміти
├─ git show [commit] → що саме змінилось
├─ Перевірити міграції/схеми/конфігурацію
└─ Прочитати змінені файли

ЕТАП 2: ЗІСТАВЛЕННЯ З ПОМИЛКОЮ
├─ Які зміни могли викликати помилку
├─ Що УЖЕ зроблено (не пропонувати повторно!)
└─ Які залежності зачеплені

ЕТАП 3: ФОРМУВАННЯ ГІПОТЕЗИ
├─ На основі РЕАЛЬНИХ даних (не здогадок!)
├─ З вказуванням confidence level (LOW/MEDIUM/HIGH)
└─ З поясненням ЧОМУ так вважаєш

ЕТАП 4: ТІЛЬКИ ПОТІМ РІШЕННЯ
└─ Запропонувати рішення з обґрунтуванням
```

---

## 🔍 Функція analyze_problem_context

```python
from typing import Dict, List
from enum import Enum


class ConfidenceLevel(Enum):
    """Рівень впевненості в рішенні."""
    LOW = "LOW"        # Потребує додаткової діагностики
    MEDIUM = "MEDIUM"  # Гіпотеза на основі часткових даних
    HIGH = "HIGH"      # Точно визначена проблема з доказами


async def analyze_problem_context(
    problem_description: str,
    project_id: str
) -> Dict:
    """
    ОБОВ'ЯЗКОВИЙ протокол аналізу проблеми ПЕРЕД рішенням.

    ⚠️ ЗАБОРОНЕНО пропонувати рішення БЕЗ цього аналізу!

    Args:
        problem_description: Опис проблеми від користувача
        project_id: ID проекту для контексту

    Returns:
        Dict з аналізом: commits, changes, root_cause, solution, confidence

    Example:
        >>> result = await analyze_problem_context(
        ...     "ERROR: relation users does not exist",
        ...     "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
        ... )
        >>> print(result['confidence'])
        ConfidenceLevel.HIGH
        >>> print(result['solution'])
        'Виправити raw SQL запит на Prisma query в invites.service.ts:12'
    """

    print("🔍 ШАГ 1: ЧИТАЮ ОСТАННІ КОМІТИ")
    print("=" * 60)

    # 1. Прочитати останні 20 комітів
    commits_output = await bash("git log --oneline -20")
    print(f"Останні коміти:\n{commits_output}\n")

    # 2. Знайти релевантні коміти (ключові слова з проблеми)
    keywords = extract_keywords(problem_description)
    print(f"Ключові слова: {', '.join(keywords)}")

    relevant_commits = []
    for keyword in keywords:
        grep_result = await bash(
            f"git log --grep='{keyword}' --oneline -20"
        )
        if grep_result:
            relevant_commits.extend(grep_result.split('\n'))

    relevant_commits = list(set(relevant_commits))  # Унікальні
    print(f"Знайдено {len(relevant_commits)} релевантних комітів")

    print("\n🔍 ШАГ 2: АНАЛІЗУЮ РЕЛЕВАНТНІ ЗМІНИ")
    print("=" * 60)

    # 3. Подивитись diff останніх релевантних комітів
    changes_analysis = []
    for commit_line in relevant_commits[:5]:  # Перші 5
        commit_hash = commit_line.split()[0]
        diff = await bash(f"git show {commit_hash}")

        print(f"\nКоміт {commit_hash}:")
        print(diff[:500] + "...\n")  # Перші 500 символів

        changes_analysis.append({
            "commit": commit_hash,
            "diff": diff
        })

    print("\n🔍 ШАГ 3: ПЕРЕВІРЯЮ ЩО УЖЕ ЗРОБЛЕНО")
    print("=" * 60)

    # 4. Перевірити міграції
    try:
        migrations = await bash("ls -la prisma/migrations/")
        print(f"Міграції:\n{migrations}\n")
    except:
        print("Міграції не знайдені або не застосовуються\n")
        migrations = None

    # 5. Перевірити схему БД
    try:
        schema = await read_file("prisma/schema.prisma")
        print(f"Схема БД (перші 500 символів):\n{schema[:500]}...\n")
    except:
        print("Схема БД не знайдена\n")
        schema = None

    print("\n🔍 ШАГ 4: АНАЛІЗУЮ ЛОГИ ПОМИЛКИ")
    print("=" * 60)

    # 6. Проаналізувати помилку з контекстом змін
    error_analysis = analyze_error_with_context(
        error_logs=problem_description,
        recent_changes=changes_analysis,
        db_schema=schema,
        migrations=migrations
    )

    print("\n✅ ШАГ 5: ФОРМУЮ ОСМИСЛЕНЕ РІШЕННЯ")
    print("=" * 60)
    print(f"Корінна причина: {error_analysis['root_cause']}")
    print(f"Рішення: {error_analysis['solution']}")
    print(f"Впевненість: {error_analysis['confidence'].value}")

    return {
        "commits_analyzed": len(relevant_commits),
        "changes_found": changes_analysis,
        "root_cause": error_analysis["root_cause"],
        "solution": error_analysis["solution"],
        "confidence": error_analysis["confidence"]
    }


def extract_keywords(text: str) -> List[str]:
    """
    Вилучити ключові слова з опису проблеми.

    Args:
        text: Опис проблеми

    Returns:
        List топ-5 ключових слів

    Example:
        >>> extract_keywords("ERROR: relation public.users does not exist")
        ['error', 'relation', 'users', 'exist']
    """

    # Видалити стоп-слова
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at"}

    words = text.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 3]

    return keywords[:5]  # Топ-5


def analyze_error_with_context(
    error_logs: str,
    recent_changes: List[Dict],
    db_schema: str,
    migrations: str
) -> Dict:
    """
    Проаналізувати помилку з урахуванням контексту змін.

    Args:
        error_logs: Логи помилки
        recent_changes: Список останніх змін (коміти + diff)
        db_schema: Вміст schema.prisma
        migrations: Вміст папки міграцій

    Returns:
        Dict: {
            "root_cause": str,
            "solution": str,
            "confidence": ConfidenceLevel
        }

    Example:
        >>> result = analyze_error_with_context(
        ...     "relation public.users does not exist",
        ...     [{"commit": "abc123", "diff": "SELECT * FROM public.users"}],
        ...     "model User { ... }",
        ...     "20250109_create_users"
        ... )
        >>> result['confidence']
        ConfidenceLevel.HIGH
    """

    # Приклад логіки аналізу: помилка з БД
    if "relation" in error_logs and "does not exist" in error_logs:
        # Перевірити чи таблиця є в схемі
        table_name = extract_table_name(error_logs)

        if db_schema and table_name.lower() in db_schema.lower():
            # Таблиця Є в схемі - проблема в запиті
            return {
                "root_cause": f"Таблиця {table_name} існує в schema.prisma, "
                             f"але запит використовує неправильний синтаксис",
                "solution": "Перевірити raw SQL запити - замінити на Prisma query",
                "confidence": ConfidenceLevel.HIGH
            }
        else:
            # Таблиці НЕМАЄ - проблема з міграцією
            return {
                "root_cause": f"Таблиця {table_name} не знайдена в schema.prisma",
                "solution": "Додати model до schema.prisma та створити міграцію",
                "confidence": ConfidenceLevel.MEDIUM
            }

    # Загальний аналіз для інших типів помилок
    return {
        "root_cause": "Потребує детального аналізу логів",
        "solution": "Додаткова діагностика необхідна",
        "confidence": ConfidenceLevel.LOW
    }


def extract_table_name(error_text: str) -> str:
    """
    Вилучити назву таблиці з помилки.

    Args:
        error_text: Текст помилки

    Returns:
        Назва таблиці або "unknown"

    Example:
        >>> extract_table_name('relation "public.users" does not exist')
        'public.users'
    """
    import re
    match = re.search(r'relation "([^"]+)"', error_text)
    return match.group(1) if match else "unknown"
```

---

## ❌ ЗАБОРОНЕНІ ФРАЗИ (говорять про здогадки)

**НІ КОЛИ не використовувати:**

- "Вероятно таблиця не існує"
- "Схоже міграція не застосувалась"
- "Можливо схема не оновлена"
- "Скоріше за все проблема в..."
- "Напевно потрібно..."
- "Здається що..."

**Чому заборонено:**
- Ці фрази говорять що агент НЕ АНАЛІЗУВАВ контекст
- Рішення на основі здогадок створюють ЩЕ БІЛЬШЕ проблем
- Доведеться виправляти у 2 рази більше

---

## ✅ ПРАВИЛЬНІ ФРАЗИ (говорять про аналіз)

**ЗАВЖДИ використовувати:**

- "Проаналізував коміт X, де додали функціонал Y"
- "В diff бачу що змінили запит Z"
- "Міграція вже застосована (див. коміт ABC)"
- "Схема містить таблицю users (перевірив schema.prisma)"
- "Реальна проблема в рядку N файлу M (див. git show)"
- "На основі аналізу змін у коміті X, бачу що..."
- "Порівнявши diff з помилкою, визначив що..."

**Чому правильно:**
- Фрази підкріплені КОНКРЕТНИМИ доказами
- Вказують на ТОЧНЕ місце проблеми
- Рішення базується на РЕАЛЬНИХ даних

---

## 📊 Приклад ПРАВИЛЬНОГО аналізу

### Ситуація:
```
Користувач: "Помилка в production: ERROR: relation 'public.users' does not exist"
```

### ❌ НЕПРАВИЛЬНА відповідь (без аналізу):
```
Агент: "Таблиця users не існує в БД.
Потрібно запустити Prisma міграції на production."
```

**Проблема:** Агент НЕ перевірив що міграція вже була!

### ✅ ПРАВИЛЬНА відповідь (з аналізом):
```
Агент: "🔍 Аналізую контекст проблеми...

ШАГ 1: Читаю останні коміти
- Коміт abc123: 'feat: add delete invite link feature'
- Коміт def456: 'fix: owner account missing'

ШАГ 2: Аналізую зміни в релевантних комітах
git show abc123:
- Додано запит: DELETE FROM invites WHERE...
- Змінено запит: SELECT owner FROM accounts...
- ЗНАЙДЕНО raw SQL: SELECT * FROM public.users

ШАГ 3: Перевіряю міграції та схему
- Міграція 20250109_create_users УЖЕ застосована ✅
- schema.prisma МІСТИТЬ model User ✅
- Production БД має таблицю users ✅

ШАГ 4: Виявлення реальної проблеми
В коміті abc123 в файлі invites.service.ts:12
використовується RAW SQL запит:
  SELECT * FROM public.users

Але в Prisma проекті потрібно використовувати:
  prisma.user.findMany()

ШАГ 5: Рішення
КОРІННА ПРИЧИНА: Використання raw SQL замість Prisma query

РІШЕННЯ: Виправити рядок 12 у invites.service.ts:
  // ❌ НЕПРАВИЛЬНО:
  await prisma.$queryRaw`SELECT * FROM public.users`

  // ✅ ПРАВИЛЬНО:
  await prisma.user.findMany()

CONFIDENCE: HIGH (бачу точний рядок у diff коміту abc123)"
```

---

## 🎯 Confidence Levels - Коли використовувати

### HIGH Confidence
**Коли:** Точно визначена проблема з конкретними доказами

**Приклади:**
- Знайшов точний рядок коду в diff
- Бачу помилку в конкретному коміті
- Міграція підтверджена, але запит неправильний

**Формат:**
```python
{
    "root_cause": "[Конкретна причина з посиланням на код]",
    "solution": "[Точне рішення з номером рядка]",
    "confidence": ConfidenceLevel.HIGH
}
```

### MEDIUM Confidence
**Коли:** Гіпотеза на основі часткових даних

**Приклади:**
- Підозра на проблему в конкретному модулі
- Є патерн помилок, але не точна локація
- Міграція не знайдена (можливо не застосована)

**Формат:**
```python
{
    "root_cause": "[Ймовірна причина з обґрунтуванням]",
    "solution": "[Рекомендоване рішення + що перевірити]",
    "confidence": ConfidenceLevel.MEDIUM
}
```

### LOW Confidence
**Коли:** Потребує додаткової діагностики

**Приклади:**
- Недостатньо інформації в логах
- Не знайдено релевантних комітів
- Проблема може бути в кількох місцях

**Формат:**
```python
{
    "root_cause": "Потребує детального аналізу",
    "solution": "[Що потрібно додатково перевірити]",
    "confidence": ConfidenceLevel.LOW
}
```

---

## 🚨 КРИТИЧНЕ ПРАВИЛО

**НІ ОДНОГО рішення без analyze_problem_context()!**

```python
# ❌ ЗАБОРОНЕНО - рішення без аналізу
async def fix_problem(error_description: str):
    # Агент одразу пропонує рішення
    return "Потрібно запустити міграції"


# ✅ ПРАВИЛЬНО - спочатку аналіз
async def fix_problem(error_description: str, project_id: str):
    # ОБОВ'ЯЗКОВО: спочатку аналіз
    analysis = await analyze_problem_context(
        problem_description=error_description,
        project_id=project_id
    )

    # ТІЛЬКИ ПОТІМ рішення на основі аналізу
    if analysis['confidence'] == ConfidenceLevel.HIGH:
        return analysis['solution']
    else:
        return f"Потребує додаткової діагностики: {analysis['root_cause']}"
```

---

## 📝 Чек-лист для агентів

При отриманні проблеми від користувача:

- [ ] Прочитав git log --oneline -20
- [ ] Знайшов релевантні коміти за ключовими словами
- [ ] Проаналізував diff змінених файлів
- [ ] Перевірив міграції/схему/конфігурацію
- [ ] Зіставив зміни з помилкою
- [ ] Сформував гіпотезу з confidence level
- [ ] Пояснив ЧОМУ так вважаю (з доказами)
- [ ] Запропонував рішення з обґрунтуванням

**Якщо хоча б 1 пункт НЕ виконаний → рішення НЕ ДАВАТИ!**

---

**Версія:** 1.0
**Дата:** 2025-10-09
**Автор:** Archon Blueprint Architect
