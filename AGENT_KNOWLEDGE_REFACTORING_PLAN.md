# План приоритетного рефакторинга 37 агентов

## 🎯 Цель рефакторинга

Преобразовать монолитные knowledge файлы агентов в модульную архитектуру для:
- ✅ Улучшения запоминаемости правил агентами (целевая метрика: 80%+ правил соблюдаются)
- ✅ Упрощения поддержки и обновления правил (одна правка → все 37 агентов обновлены)
- ✅ Сокращения дублирования кода (с 4,810 до 401 строк общих правил)
- ✅ Интеграции 8 последних улучшений из AGENT_IMPROVEMENTS_ANALYSIS.md

---

## 📊 Текущее состояние

### Статистика до рефакторинга:
- **Всего агентов:** 37 (7 Archon + 18 Pattern + 12 Specialized)
- **Средний размер файла:** 712 строк (130 дубликатов + 582 уникальных)
- **Дублирование:** ~130 строк × 37 = 4,810 строк
- **Проблемы:**
  - Низкая запоминаемость правил агентами
  - Сложность обновления (37 файлов на правку)
  - Отсутствие 8 последних улучшений в агентах

### Статистика после рефакторинга:
- **Средний размер файла:** ~630 строк (50 промпт + 580 доменные знания)
- **Общие модули:** 401 строка (одна версия для всех)
- **Экономия:** 4,409 строк дублирования
- **Интеграция:** Все 8 улучшений из AGENT_IMPROVEMENTS_ANALYSIS.md

---

## 🗂️ Классификация агентов

### Группа A: Archon базовые агенты (7 агентов)
**Характеристика:** Ядро системы, используются постоянно

1. `archon_analysis_lead` - Анализ требований (509+ строк)
2. `archon_blueprint_architect` - Архитектура (1402+ строк) ⚠️ САМЫЙ БОЛЬШОЙ
3. `archon_implementation_engineer` - Разработка
4. `archon_quality_guardian` - Тестирование
5. `archon_deployment_engineer` - DevOps
6. `archon_project_manager` - Управление проектами
7. `archon_common` - Общие задачи

**Приоритет:** 🔴 ВЫСОКИЙ (Фаза 1)
**Причина:** Используются чаще всех, влияют на workflow всех остальных

---

### Группа B: Specialized агенты (12 агентов)
**Характеристика:** Универсальные, применимы к разным проектам

1. `analytics_tracking_agent` - Аналитика
2. `api_development_agent` - API разработка
3. `community_management_agent` - Управление сообществом
4. `mcp_configuration_agent` - Настройка MCP серверов
5. `payment_integration_agent` - Платёжные интеграции (890+ строк)
6. `performance_optimization_agent` - Оптимизация производительности (1026+ строк) ⚠️ САМЫЙ БОЛЬШОЙ
7. `prisma_database_agent` - Prisma ORM
8. `pwa_mobile_agent` - PWA разработка
9. `queue_worker_agent` - Фоновые задачи
10. `rag_agent` - Семантический поиск
11. `security_audit_agent` - Security аудит (611+ строк)
12. `typescript_architecture_agent` - TypeScript архитектура (666+ строк)
13. `uiux_enhancement_agent` - UI/UX улучшения

**Приоритет:** 🟡 СРЕДНИЙ (Фаза 2)
**Причина:** Используются часто, но не критичны для основного workflow

---

### Группа C: Pattern агенты (18 агентов)
**Характеристика:** Специализированы под проект PatternShift

1. `pattern_age_adaptation_agent` (570+ строк)
2. `pattern_cultural_adaptation_agent`
3. `pattern_ericksonian_hypnosis_scriptwriter_agent`
4. `pattern_exercise_architect_agent`
5. `pattern_feedback_orchestrator_agent`
6. `pattern_gamification_architect_agent`
7. `pattern_gender_adaptation_agent`
8. `pattern_integration_synthesizer_agent`
9. `pattern_metaphor_weaver_agent`
10. `pattern_microhabit_designer_agent`
11. `pattern_nlp_technique_master_agent`
12. `pattern_orchestrator_agent`
13. `pattern_progress_narrator_agent`
14. `pattern_safety_protocol_agent`
15. `pattern_scientific_validator_agent`
16. `pattern_test_architect_agent`
17. `pattern_transition_craftsman_agent`
18. `pattern_vak_adaptation_agent`

**Приоритет:** 🟢 НИЗКИЙ (Фаза 3)
**Причина:** Проект-специфичны, используются реже, не публикуются в git

---

## 📅 Фазы рефакторинга

### ФАЗА 0: Подготовка (ВЫПОЛНЕНО ✅)
**Сроки:** 1 день (2025-10-14)

- [x] Анализ 6 примеров агентов
- [x] Выявление общих паттернов (130 строк дублирования)
- [x] Разработка модульной архитектуры
- [x] Создание `agents/_shared/agent_common_rules.md`
- [x] Создание `agents/_shared/agent_knowledge_template.md`
- [x] Интеграция 8 улучшений из AGENT_IMPROVEMENTS_ANALYSIS.md
- [x] Добавление описания всех MCP серверов

**Результат:** Готова инфраструктура для рефакторинга

---

### ФАЗА 1: Archon базовые агенты (7 агентов)
**Сроки:** 2-3 дня
**Приоритет:** 🔴 КРИТИЧЕСКИЙ

#### Порядок рефакторинга:

1. **archon_blueprint_architect** (день 1, утро)
   - Причина первым: самый большой (1402+ строк), архитектор системы
   - Особенности: содержит стратегии A/B/C для работы с модулями
   - Цель: проверить шаблон на самом сложном кейсе

2. **archon_analysis_lead** (день 1, вечер)
   - Причина вторым: базовый агент, начало цепочки (анализ → архитектура → разработка)
   - Особенности: декомпозиция требований, планирование
   - Цель: рефакторинг от начала процесса

3. **archon_implementation_engineer** (день 2, утро)
   - Причина третьим: основной разработчик, самая частая роль
   - Особенности: кодирование, стандарты, тестирование
   - Цель: ключевая роль для большинства задач

4. **archon_quality_guardian** (день 2, вечер)
   - Причина четвёртым: завершающий этап разработки
   - Особенности: тестирование, code review
   - Цель: контроль качества после разработки

5. **archon_deployment_engineer** (день 3, утро)
   - Причина пятым: финальный этап деплоя
   - Особенности: DevOps, CI/CD
   - Цель: завершение цепочки разработки

6. **archon_project_manager** (день 3, вечер)
   - Причина шестым: оркестрирование всех остальных
   - Особенности: приоритизация, делегирование
   - Цель: координация после рефакторинга основных ролей

7. **archon_common** (день 3, финал)
   - Причина последним: общие задачи, используется редко
   - Особенности: универсальность
   - Цель: завершение базовой группы

#### Чек-лист рефакторинга каждого агента:

```markdown
- [ ] Прочитать текущий knowledge файл
- [ ] Извлечь системный промпт (первые ~50 строк после хедера)
- [ ] Извлечь уникальные доменные знания (остальное)
- [ ] Создать новый файл на основе agent_knowledge_template.md
- [ ] Вставить системный промпт роли
- [ ] Вставить доменные знания
- [ ] Добавить ссылку на agents/_shared/agent_common_rules.md
- [ ] Проверить наличие роль-специфичных чек-листов
- [ ] Удалить дублирующиеся общие правила (130 строк)
- [ ] Сохранить оригинал как .backup
- [ ] Протестировать агента на простой задаче
- [ ] Убедиться что агент читает общие правила
- [ ] Git commit: "refactor: [agent_name] knowledge to modular architecture"
- [ ] Push в remote
```

#### Метрики успеха Фазы 1:

- ✅ Размер файлов сокращён с ~700 до ~630 строк
- ✅ Все 7 агентов ссылаются на общие правила
- ✅ Тесты показывают соблюдение правил 80%+
- ✅ Агенты применяют 8 новых улучшений
- ✅ Коммиты и push созданы для каждого агента

---

### ФАЗА 2: Specialized агенты (13 агентов)
**Сроки:** 3-4 дня
**Приоритет:** 🟡 СРЕДНИЙ

#### Порядок рефакторинга (по размеру, от большего к меньшему):

**День 4:**
1. `performance_optimization_agent` (1026+ строк) - самый большой
2. `payment_integration_agent` (890+ строк)
3. `typescript_architecture_agent` (666+ строк)

**День 5:**
4. `security_audit_agent` (611+ строк)
5. `uiux_enhancement_agent`
6. `rag_agent`

**День 6:**
7. `prisma_database_agent`
8. `api_development_agent`
9. `pwa_mobile_agent`

**День 7:**
10. `queue_worker_agent`
11. `analytics_tracking_agent`
12. `community_management_agent`
13. `mcp_configuration_agent`

#### Особенности Specialized агентов:
- Больше доменных знаний (400-900 строк уникального контента)
- Специализированные технологии и инструменты
- Взаимодействие с внешними системами (Stripe, Railway, PostgreSQL, etc.)
- Более сложные чек-листы проверки

#### Метрики успеха Фазы 2:
- ✅ Все 13 агентов рефакторены
- ✅ Средний размер: ~850 строк (50 промпт + 800 домен)
- ✅ Связь с Archon агентами через общие правила
- ✅ Специализированные чек-листы сохранены

---

### ФАЗА 3: Pattern агенты (18 агентов)
**Сроки:** 4-5 дней
**Приоритет:** 🟢 НИЗКИЙ (можно отложить)

#### Порядок рефакторинга (по логическим группам):

**День 8: Адаптация контента**
1. `pattern_age_adaptation_agent` (570+ строк)
2. `pattern_gender_adaptation_agent`
3. `pattern_cultural_adaptation_agent`
4. `pattern_vak_adaptation_agent`

**День 9: Создание контента**
5. `pattern_ericksonian_hypnosis_scriptwriter_agent`
6. `pattern_metaphor_weaver_agent`
7. `pattern_progress_narrator_agent`
8. `pattern_transition_craftsman_agent`

**День 10: Архитектура и дизайн**
9. `pattern_exercise_architect_agent`
10. `pattern_gamification_architect_agent`
11. `pattern_microhabit_designer_agent`
12. `pattern_test_architect_agent`

**День 11: Управление и контроль**
13. `pattern_orchestrator_agent`
14. `pattern_feedback_orchestrator_agent`
15. `pattern_integration_synthesizer_agent`
16. `pattern_safety_protocol_agent`

**День 12: Специализированные**
17. `pattern_nlp_technique_master_agent`
18. `pattern_scientific_validator_agent`

#### Особенности Pattern агентов:
- Проект-специфичны (PatternShift)
- НЕ публикуются в git (локальная разработка)
- Роль-ориентированные (для переключения Claude)
- Работают с модулями PatternShift
- Минимум технического кода

#### Метрики успеха Фазы 3:
- ✅ Все 18 агентов рефакторены
- ✅ Средний размер: ~620 строк (50 промпт + 570 домен)
- ✅ Общие правила применимы (кроме git push)
- ✅ Pattern-специфичные секции сохранены

---

## 🔧 Инструменты и скрипты

### Автоматизация рефакторинга:

```python
# refactor_agent_knowledge.py
"""
Скрипт для автоматизации рефакторинга knowledge файлов.

Usage:
    python refactor_agent_knowledge.py archon_analysis_lead
    python refactor_agent_knowledge.py --batch archon_*
"""

import re
from pathlib import Path
from typing import Tuple

def extract_sections(content: str) -> Tuple[str, str, str]:
    """
    Извлечь секции из knowledge файла.

    Returns:
        (header, system_prompt, domain_knowledge)
    """
    # Извлечь хедер (первые 130 строк дубликата)
    header_pattern = r"^(# ⚠️.*?^---\n\n)"
    header_match = re.search(header_pattern, content, re.MULTILINE | re.DOTALL)

    # Извлечь системный промпт (после хедера, ~50 строк)
    prompt_pattern = r"^## 🎭 СИСТЕМНЫЙ ПРОМПТ.*?(?=^##|\Z)"
    prompt_match = re.search(prompt_pattern, content, re.MULTILINE | re.DOTALL)

    # Остальное = доменные знания
    domain_start = prompt_match.end() if prompt_match else len(header_match.group(0))
    domain_knowledge = content[domain_start:].strip()

    return (
        header_match.group(0) if header_match else "",
        prompt_match.group(0) if prompt_match else "",
        domain_knowledge
    )

def create_new_knowledge(
    agent_name: str,
    system_prompt: str,
    domain_knowledge: str,
    template_path: Path
) -> str:
    """
    Создать новый knowledge файл на основе шаблона.
    """
    template = template_path.read_text(encoding='utf-8')

    # Заменить плейсхолдеры
    new_content = template.replace(
        "[НАЗВАНИЕ РОЛИ]", agent_name.replace("_", " ").title()
    )

    # Вставить системный промпт
    new_content = new_content.replace(
        "## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: [НАЗВАНИЕ РОЛИ]",
        system_prompt
    )

    # Добавить доменные знания после промпта
    insert_point = new_content.find("## 🔍 ДОМЕННЫЕ ЗНАНИЯ")
    if insert_point != -1:
        new_content = (
            new_content[:insert_point] +
            domain_knowledge + "\n\n" +
            new_content[insert_point:]
        )

    return new_content

def refactor_agent(agent_name: str, dry_run: bool = False):
    """
    Рефакторить один агент.
    """
    base_path = Path("agents")
    agent_path = base_path / f"{agent_name}" / "knowledge"
    knowledge_file = agent_path / f"{agent_name}_knowledge.md"

    if not knowledge_file.exists():
        print(f"❌ Файл не найден: {knowledge_file}")
        return

    # Прочитать текущий файл
    content = knowledge_file.read_text(encoding='utf-8')
    print(f"📖 Читаю {knowledge_file} ({len(content)} символов)")

    # Извлечь секции
    header, system_prompt, domain_knowledge = extract_sections(content)
    print(f"  ✂️ Header: {len(header)} символов")
    print(f"  ✂️ Prompt: {len(system_prompt)} символов")
    print(f"  ✂️ Domain: {len(domain_knowledge)} символов")

    # Создать новый файл
    template = Path("agents/_shared/agent_knowledge_template.md")
    new_content = create_new_knowledge(
        agent_name, system_prompt, domain_knowledge, template
    )
    print(f"  📝 Новый файл: {len(new_content)} символов")
    print(f"  💾 Экономия: {len(content) - len(new_content)} символов")

    if not dry_run:
        # Сохранить backup
        backup_file = knowledge_file.with_suffix('.md.backup')
        knowledge_file.rename(backup_file)
        print(f"  💾 Backup: {backup_file}")

        # Записать новый файл
        knowledge_file.write_text(new_content, encoding='utf-8')
        print(f"  ✅ Записано: {knowledge_file}")
    else:
        print(f"  🔍 DRY RUN - изменения не применены")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python refactor_agent_knowledge.py <agent_name>")
        sys.exit(1)

    agent = sys.argv[1]
    refactor_agent(agent, dry_run="--dry-run" in sys.argv)
```

### Валидация после рефакторинга:

```python
# validate_refactored_agents.py
"""
Проверить что рефакторинг выполнен корректно.

Usage:
    python validate_refactored_agents.py --phase 1
    python validate_refactored_agents.py --all
"""

from pathlib import Path
from typing import List, Dict

def validate_agent(agent_name: str) -> Dict[str, bool]:
    """
    Проверить один агент.

    Returns:
        {
            'has_common_rules_link': bool,
            'no_duplicated_header': bool,
            'has_system_prompt': bool,
            'has_domain_knowledge': bool,
            'size_reduced': bool
        }
    """
    agent_path = Path(f"agents/{agent_name}/knowledge/{agent_name}_knowledge.md")
    backup_path = agent_path.with_suffix('.md.backup')

    if not agent_path.exists():
        return {'error': f'File not found: {agent_path}'}

    content = agent_path.read_text(encoding='utf-8')
    backup_content = backup_path.read_text(encoding='utf-8') if backup_path.exists() else ""

    return {
        'has_common_rules_link': '../_shared/agent_common_rules.md' in content,
        'no_duplicated_header': '⚠️ КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ' not in content,
        'has_system_prompt': '## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ' in content,
        'has_domain_knowledge': '## 🔍 ДОМЕННЫЕ ЗНАНИЯ' in content,
        'size_reduced': len(content) < len(backup_content) if backup_content else False
    }

def validate_phase(phase: int) -> List[Dict]:
    """
    Проверить все агенты фазы.
    """
    agents = {
        1: [
            'archon_blueprint_architect',
            'archon_analysis_lead',
            'archon_implementation_engineer',
            'archon_quality_guardian',
            'archon_deployment_engineer',
            'archon_project_manager',
            'archon_common'
        ],
        2: [
            'performance_optimization_agent',
            'payment_integration_agent',
            'typescript_architecture_agent',
            'security_audit_agent',
            # ... rest of specialized agents
        ],
        3: [
            'pattern_age_adaptation_agent',
            'pattern_gender_adaptation_agent',
            # ... rest of pattern agents
        ]
    }

    results = []
    for agent in agents.get(phase, []):
        validation = validate_agent(agent)
        validation['agent'] = agent
        results.append(validation)

    return results

if __name__ == "__main__":
    import sys

    phase = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == '--phase' else None

    if phase:
        results = validate_phase(phase)
        print(f"\n📊 Validation Results - Phase {phase}:\n")

        for result in results:
            agent = result.pop('agent')
            all_passed = all(result.values())
            status = "✅" if all_passed else "❌"

            print(f"{status} {agent}")
            if not all_passed:
                for check, passed in result.items():
                    if not passed:
                        print(f"   ❌ {check}")

        total = len(results)
        passed = sum(1 for r in results if all(v for k, v in r.items() if k != 'agent'))
        print(f"\n📈 Success Rate: {passed}/{total} ({passed/total*100:.1f}%)")
```

---

## 📈 Метрики успеха всего рефакторинга

### Количественные метрики:

- ✅ **100% агентов рефакторены** (37/37)
- ✅ **Средний размер файла:** ~650 строк (было ~712)
- ✅ **Дублирование:** 401 строка (было 4,810)
- ✅ **Экономия:** 4,409 строк (91.7%)
- ✅ **Общие модули:** 1 файл навигации + 401 строка правил

### Качественные метрики:

- ✅ **Соблюдение правил:** 80%+ (было ~50%)
- ✅ **Скорость обновления:** 1 файл (было 37 файлов)
- ✅ **Время запоминания:** -60% (за счёт фокусировки)
- ✅ **Интеграция улучшений:** Все 8 из AGENT_IMPROVEMENTS_ANALYSIS.md
- ✅ **Консистентность:** 100% агентов используют одни правила

### Тесты верификации:

```python
# test_agent_compliance.py
"""
Тесты проверки соблюдения правил агентами после рефакторинга.
"""

def test_role_switching_compliance():
    """Агент переключается в роль перед работой."""
    agent = get_agent('archon_analysis_lead')
    task = create_test_task("Проанализируй требования")

    response = agent.execute(task)

    assert "🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ" in response
    assert "📋 Моя экспертиза:" in response
    assert "✅ Готов выполнить задачу" in response

def test_todowrite_creation():
    """Агент создаёт микрозадачи через TodoWrite."""
    agent = get_agent('archon_implementation_engineer')
    task = create_test_task("Создай новый feature")

    with monitor_tool_usage() as monitor:
        agent.execute(task)

    assert monitor.tool_called('TodoWrite')
    assert monitor.call_count('TodoWrite') >= 1

def test_post_task_checklist():
    """Последний пункт TodoWrite - Post-Task Checklist."""
    agent = get_agent('archon_quality_guardian')
    task = create_test_task("Протестируй feature")

    todos = agent.get_todos_for_task(task)
    last_todo = todos[-1]

    assert "Post-Task Checklist" in last_todo['content']
    assert "10_post_task_checklist.md" in last_todo['content']

def test_no_token_economy():
    """Агент не использует '...' для экономии токенов."""
    agent = get_agent('archon_blueprint_architect')
    task = create_test_task("Создай модуль архитектуры")

    code = agent.execute(task)

    assert "..." not in code  # Не должно быть троеточий в коде
    assert len(code.split('\n')) > 50  # Полный код, не сокращённый

def test_reads_common_rules():
    """Агент читает общие правила из _shared."""
    agent = get_agent('payment_integration_agent')

    with monitor_file_access() as monitor:
        agent.initialize()

    assert monitor.file_read('agents/_shared/agent_common_rules.md')

# ... остальные тесты для 8 улучшений
```

---

## 🚀 Следующие шаги после рефакторинга

### 1. Мониторинг и метрики (недели 1-2 после завершения)
- Отслеживание соблюдения правил в реальных задачах
- Сбор обратной связи от пользователей
- Анализ ошибок и несоответствий

### 2. Итерации и улучшения (недели 3-4)
- Корректировка общих правил на основе метрик
- Добавление недостающих секций в шаблон
- Оптимизация размера модулей

### 3. Документация (неделя 5)
- Обновление README агентов
- Создание гайдов по использованию
- Видео-туториалы переключения в роль

### 4. Масштабирование (неделя 6+)
- Применение модульности к новым агентам
- Создание генератора агентов на основе шаблона
- Автоматизация валидации при создании

---

## 📚 Приложения

### Приложение A: Структура репозитория после рефакторинга

```
agent-factory/
└── use-cases/
    └── agent-factory-with-subagents/
        ├── .claude/
        │   └── rules/
        │       ├── 01_role_switching.md
        │       ├── 02_workflow_rules.md
        │       ├── 02a_project_context_management.md ← НОВОЕ
        │       ├── ... (остальные 13 модулей)
        │       └── 15_blueprint_architect_rules.md
        ├── agents/
        │   ├── _shared/                              ← НОВОЕ
        │   │   ├── agent_common_rules.md             ← НОВОЕ (401 строка)
        │   │   └── agent_knowledge_template.md       ← НОВОЕ (шаблон)
        │   ├── archon_analysis_lead/
        │   │   └── knowledge/
        │   │       ├── archon_analysis_lead_knowledge.md       (630 строк, было 509)
        │   │       └── archon_analysis_lead_knowledge.md.backup
        │   ├── archon_blueprint_architect/
        │   │   └── knowledge/
        │   │       ├── archon_blueprint_architect_knowledge.md (650 строк, было 1402)
        │   │       └── archon_blueprint_architect_knowledge.md.backup
        │   ├── ... (остальные 35 агентов)
        │   └── pattern_vak_adaptation_agent/
        │       └── knowledge/
        │           ├── pattern_vak_adaptation_agent_knowledge.md
        │           └── pattern_vak_adaptation_agent_knowledge.md.backup
        └── AGENT_KNOWLEDGE_REFACTORING_PLAN.md       ← ЭТОТ ФАЙЛ
```

### Приложение B: Контрольный чек-лист полного рефакторинга

**ФАЗА 0: Подготовка**
- [x] Анализ примеров агентов
- [x] Создание модульной архитектуры
- [x] Создание `agent_common_rules.md`
- [x] Создание `agent_knowledge_template.md`
- [x] Интеграция 8 улучшений
- [x] Добавление описания MCP серверов

**ФАЗА 1: Archon агенты (7)**
- [ ] archon_blueprint_architect
- [ ] archon_analysis_lead
- [ ] archon_implementation_engineer
- [ ] archon_quality_guardian
- [ ] archon_deployment_engineer
- [ ] archon_project_manager
- [ ] archon_common

**ФАЗА 2: Specialized агенты (13)**
- [ ] performance_optimization_agent
- [ ] payment_integration_agent
- [ ] typescript_architecture_agent
- [ ] security_audit_agent
- [ ] uiux_enhancement_agent
- [ ] rag_agent
- [ ] prisma_database_agent
- [ ] api_development_agent
- [ ] pwa_mobile_agent
- [ ] queue_worker_agent
- [ ] analytics_tracking_agent
- [ ] community_management_agent
- [ ] mcp_configuration_agent

**ФАЗА 3: Pattern агенты (18)**
- [ ] pattern_age_adaptation_agent
- [ ] pattern_gender_adaptation_agent
- [ ] pattern_cultural_adaptation_agent
- [ ] pattern_vak_adaptation_agent
- [ ] pattern_ericksonian_hypnosis_scriptwriter_agent
- [ ] pattern_metaphor_weaver_agent
- [ ] pattern_progress_narrator_agent
- [ ] pattern_transition_craftsman_agent
- [ ] pattern_exercise_architect_agent
- [ ] pattern_gamification_architect_agent
- [ ] pattern_microhabit_designer_agent
- [ ] pattern_test_architect_agent
- [ ] pattern_orchestrator_agent
- [ ] pattern_feedback_orchestrator_agent
- [ ] pattern_integration_synthesizer_agent
- [ ] pattern_safety_protocol_agent
- [ ] pattern_nlp_technique_master_agent
- [ ] pattern_scientific_validator_agent

**ВЕРИФИКАЦИЯ:**
- [ ] Запущены все тесты валидации
- [ ] Success rate 95%+
- [ ] Все backups созданы
- [ ] Все изменения закоммичены
- [ ] Обновлён update-agent-registry.py

**МОНИТОРИНГ (после завершения):**
- [ ] Неделя 1: Сбор метрик соблюдения правил
- [ ] Неделя 2: Анализ ошибок и несоответствий
- [ ] Неделя 3-4: Итерации и улучшения
- [ ] Неделя 5: Документация и гайды
- [ ] Неделя 6+: Масштабирование на новые агенты

---

**Версия плана:** 1.0
**Дата создания:** 2025-10-14
**Автор:** Archon Blueprint Architect
**Статус:** Готов к выполнению (Фаза 0 завершена)
