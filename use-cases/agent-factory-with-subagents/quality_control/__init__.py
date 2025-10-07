# -*- coding: utf-8 -*-
"""
Инструменты для роли Quality Guardian.

Эти инструменты помогают мне (Claude) когда я переключаюсь в роль Quality Guardian.

Использование:
    from quality_control.tools import run_quality_audit

    report = run_quality_audit("path/to/project")
"""

from .tools import (
    run_quality_audit,
    check_role_switching,
    check_universality,
    check_code_quality,
    check_architecture,
    check_documentation,
    check_testing,
    create_archon_tasks_for_problems
)

from .checklists import (
    ROLE_SWITCHING_CHECKLIST,
    UNIVERSALITY_CHECKLIST,
    CODE_QUALITY_CHECKLIST,
    ARCHITECTURE_CHECKLIST,
    DOCUMENTATION_CHECKLIST,
    TESTING_CHECKLIST,
    FULL_QUALITY_CHECKLIST
)

__all__ = [
    # Инструменты
    "run_quality_audit",
    "check_role_switching",
    "check_universality",
    "check_code_quality",
    "check_architecture",
    "check_documentation",
    "check_testing",
    "create_archon_tasks_for_problems",

    # Чеклисты
    "ROLE_SWITCHING_CHECKLIST",
    "UNIVERSALITY_CHECKLIST",
    "CODE_QUALITY_CHECKLIST",
    "ARCHITECTURE_CHECKLIST",
    "DOCUMENTATION_CHECKLIST",
    "TESTING_CHECKLIST",
    "FULL_QUALITY_CHECKLIST"
]

__version__ = "1.0.0"
