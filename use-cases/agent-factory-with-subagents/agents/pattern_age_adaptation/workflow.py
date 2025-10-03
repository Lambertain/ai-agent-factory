# -*- coding: utf-8 -*-
"""
Специализированный workflow Pattern Age Adaptation Agent.

Реализует workflow из pattern-agents-complete-workflow.md
для возрастной адаптации модулей на Шаге 4.2 (Дни 29-32).
"""

from typing import Dict, List, Any
from pathlib import Path
import json
import logging

from .dependencies import PatternAgeAdaptationDependencies

logger = logging.getLogger(__name__)


class AgeAdaptationWorkflow:
    """
    Workflow возрастной адаптации модулей PatternShift.

    Согласно pattern-agents-complete-workflow.md:
    - Шаг 4.2 (Дни 29-32): Возрастная адаптация
    - Входные данные: Гендерно-адаптированные модули (3 версии каждого базового)
    - Выходные данные: 5 возрастных версий каждого входного модуля
    - Следующий агент: Pattern VAK Adaptation Specialist (Шаг 4.3)
    """

    def __init__(self, deps: PatternAgeAdaptationDependencies):
        """
        Инициализация workflow.

        Args:
            deps: Зависимости агента
        """
        self.deps = deps
        self.input_modules_processed = 0
        self.output_modules_created = 0

    async def process_module_batch(
        self,
        modules: List[Dict[str, Any]],
        module_type: str
    ) -> List[Dict[str, Any]]:
        """
        Обработать пакет модулей для возрастной адаптации.

        Args:
            modules: Список гендерно-адаптированных модулей
            module_type: Тип модулей (nlp_technique, hypnosis_script и т.д.)

        Returns:
            Список адаптированных модулей (каждый модуль × 5 возрастных версий)
        """
        adapted_modules = []

        for module in modules:
            # Создаем 5 возрастных версий каждого модуля
            for age_version in self.deps.age_versions:
                adapted = await self._adapt_module(module, age_version, module_type)
                adapted_modules.append(adapted)
                self.output_modules_created += 1

            self.input_modules_processed += 1

        logger.info(
            f"Обработано {self.input_modules_processed} гендерных модулей типа {module_type}, "
            f"создано {self.output_modules_created} возрастных версий"
        )

        return adapted_modules

    async def _adapt_module(
        self,
        module: Dict[str, Any],
        age_version: str,
        module_type: str
    ) -> Dict[str, Any]:
        """
        Адаптировать один модуль под возрастную версию.

        Args:
            module: Гендерно-адаптированный модуль
            age_version: Возрастная версия (teens, young_adults и т.д.)
            module_type: Тип модуля

        Returns:
            Адаптированный модуль
        """
        adapted = module.copy()
        adapted["age_version"] = age_version
        adapted["age_range"] = self.deps.get_age_range(age_version)
        adapted["developmental_task"] = self.deps.get_developmental_task(age_version)
        adapted["parent_module_id"] = module.get("module_id", "unknown")
        adapted["module_id"] = f"{module.get('module_id', 'unknown')}_{age_version}"
        adapted["age_adaptations"] = []

        # Применяем возрастные адаптации в зависимости от версии
        if age_version == "teens":
            adapted = self._apply_teens_adaptations(adapted, module_type)
        elif age_version == "young_adults":
            adapted = self._apply_young_adults_adaptations(adapted, module_type)
        elif age_version == "early_middle_age":
            adapted = self._apply_early_middle_adaptations(adapted, module_type)
        elif age_version == "middle_age":
            adapted = self._apply_middle_age_adaptations(adapted, module_type)
        else:  # seniors
            adapted = self._apply_seniors_adaptations(adapted, module_type)

        # Валидация на соответствие задачам развития
        if self.deps.enable_developmental_validation:
            adapted["developmental_validation"] = self._validate_developmental_fit(adapted)

        return adapted

    def _apply_teens_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить адаптации для подростков."""
        adaptations = []

        # Подростковые паттерны коммуникации
        replacements = {
            "достигните": "открой в себе",
            "проанализируйте": "посмотри на это так",
            "осознайте": "пойми",
            "эффективность": "крутой результат",
            "стратегия": "план действий",
            "ресурсное состояние": "когда ты на подъеме"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': адаптация для подростков")
                    module[key] = value

        module["age_adaptations"] = adaptations
        module["adaptation_focus"] = "Поиск идентичности, энергичность, близость к молодежи"

        return module

    def _apply_young_adults_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить адаптации для молодых взрослых."""
        adaptations = []

        replacements = {
            "детский опыт": "предыдущий опыт",
            "мудрость лет": "накопленный опыт",
            "в вашем возрасте": "на этом этапе жизни",
            "долгосрочные цели": "цели на ближайшие годы"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': адаптация для молодых взрослых")
                    module[key] = value

        module["age_adaptations"] = adaptations
        module["adaptation_focus"] = "Карьера, отношения, самостоятельность"

        return module

    def _apply_early_middle_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить адаптации для раннего среднего возраста."""
        adaptations = []

        replacements = {
            "поиск себя": "оптимизация ролей",
            "кто я": "баланс профессионального и личного",
            "экспериментируй": "стратегически выбирай"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': адаптация для раннего среднего возраста")
                    module[key] = value

        module["age_adaptations"] = adaptations
        module["adaptation_focus"] = "Work-life balance, системный подход, долгосрочные стратегии"

        return module

    def _apply_middle_age_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить адаптации для среднего возраста."""
        adaptations = []

        replacements = {
            "достижение целей": "вклад в развитие других",
            "личный успех": "создание наследия",
            "карьерный рост": "передача опыта"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': адаптация для среднего возраста")
                    module[key] = value

        module["age_adaptations"] = adaptations
        module["adaptation_focus"] = "Генеративность, наставничество, смысл и наследие"

        return module

    def _apply_seniors_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить адаптации для старшего возраста."""
        adaptations = []

        replacements = {
            "начни путь": "интегрируй опыт",
            "открой новое": "переосмысли прожитое",
            "достигни цели": "найди мудрость в пройденном",
            "быстрый результат": "глубокое понимание"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': адаптация для старшего возраста")
                    module[key] = value

        module["age_adaptations"] = adaptations
        module["adaptation_focus"] = "Интеграция опыта, мудрость, принятие"

        return module

    def _validate_developmental_fit(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидировать модуль на соответствие задачам развития.

        Args:
            module: Модуль для проверки

        Returns:
            Результаты валидации
        """
        text = str(module).lower()
        age_version = module.get("age_version", "")
        developmental_task = self.deps.get_developmental_task(age_version)

        # Критерии для каждой задачи развития
        developmental_criteria = {
            "identity_formation": ["поиск себя", "идентичност", "кто я", "самоопределени"],
            "intimacy_vs_isolation": ["отношени", "близость", "связ", "партнер"],
            "generativity_beginning": ["вклад", "создани", "баланс", "развити"],
            "generativity_peak": ["наставничеств", "передач", "наследи", "смысл"],
            "integrity_vs_despair": ["приняти", "интеграци", "мудрост", "жизненный путь"]
        }

        criteria = developmental_criteria.get(developmental_task, [])
        matches = [c for c in criteria if c in text]

        return {
            "is_valid": len(matches) > 0,
            "developmental_task": developmental_task,
            "criteria_matched": matches,
            "validated_at": "age_adaptation_stage"
        }

    async def save_adapted_modules(
        self,
        adapted_modules: List[Dict[str, Any]],
        output_dir: str = "adapted_modules/age"
    ) -> str:
        """
        Сохранить адаптированные модули в файловую систему.

        Args:
            adapted_modules: Список адаптированных модулей
            output_dir: Директория для сохранения

        Returns:
            Путь к сохраненным модулям
        """
        output_path = Path(self.deps.project_path) / output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        # Группируем по типу модуля и возрастной версии
        modules_by_type_and_age = {}
        for module in adapted_modules:
            module_type = module.get("module_type", "unknown")
            age_version = module.get("age_version", "unknown")
            key = f"{module_type}_{age_version}"

            if key not in modules_by_type_and_age:
                modules_by_type_and_age[key] = []
            modules_by_type_and_age[key].append(module)

        # Сохраняем каждую группу в отдельный файл
        saved_files = []
        for key, modules in modules_by_type_and_age.items():
            file_path = output_path / f"{key}_age_adapted.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(modules, f, indent=2, ensure_ascii=False)
            saved_files.append(str(file_path))
            logger.info(f"Сохранено {len(modules)} модулей группы {key} в {file_path}")

        return str(output_path)

    def get_workflow_stats(self) -> Dict[str, Any]:
        """
        Получить статистику выполнения workflow.

        Returns:
            Статистика обработки
        """
        return {
            "input_modules_processed": self.input_modules_processed,
            "output_modules_created": self.output_modules_created,
            "multiplication_factor": 5,  # каждый модуль × 5 возрастных версий
            "age_versions": self.deps.age_versions,
            "age_ranges": self.deps.age_ranges,
            "developmental_tasks": self.deps.developmental_tasks,
            "developmental_validation_enabled": self.deps.enable_developmental_validation,
            "workflow_stage": "Step 4.2 - Age Adaptation (Days 29-32)",
            "next_agent": "Pattern VAK Adaptation Specialist (Step 4.3)"
        }
