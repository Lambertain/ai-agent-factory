# -*- coding: utf-8 -*-
"""
Специализированный workflow Pattern Gender Adaptation Agent.

Реализует workflow из pattern-agents-complete-workflow.md
для гендерной адаптации модулей на Шаге 4.1 (Дни 25-28).
"""

from typing import Dict, List, Any
from pathlib import Path
import json
import logging

from .dependencies import PatternGenderAdaptationDependencies

logger = logging.getLogger(__name__)


class GenderAdaptationWorkflow:
    """
    Workflow гендерной адаптации модулей PatternShift.

    Согласно pattern-agents-complete-workflow.md:
    - Шаг 4.1 (Дни 25-28): Гендерная адаптация
    - Входные данные: ВСЕ базовые модули после Фазы 2 (НЛП, гипноз, упражнения, и т.д.)
    - Выходные данные: 3 версии каждого модуля (masculine, feminine, neutral)
    - Следующий агент: Pattern Age Adaptation Agent (Шаг 4.2)
    """

    def __init__(self, deps: PatternGenderAdaptationDependencies):
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
        Обработать пакет модулей для гендерной адаптации.

        Args:
            modules: Список базовых модулей
            module_type: Тип модулей (nlp_technique, hypnosis_script, exercise и т.д.)

        Returns:
            Список адаптированных модулей (каждый модуль × 3 версии)
        """
        adapted_modules = []

        for module in modules:
            # Создаем 3 версии каждого модуля
            for version in self.deps.gender_versions:
                adapted = await self._adapt_module(module, version, module_type)
                adapted_modules.append(adapted)
                self.output_modules_created += 1

            self.input_modules_processed += 1

        logger.info(
            f"Обработано {self.input_modules_processed} модулей типа {module_type}, "
            f"создано {self.output_modules_created} адаптированных версий"
        )

        return adapted_modules

    async def _adapt_module(
        self,
        module: Dict[str, Any],
        version: str,
        module_type: str
    ) -> Dict[str, Any]:
        """
        Адаптировать один модуль под гендерную версию.

        Args:
            module: Базовый модуль
            version: Гендерная версия (masculine/feminine/neutral)
            module_type: Тип модуля

        Returns:
            Адаптированный модуль
        """
        adapted = module.copy()
        adapted["gender_version"] = version
        adapted["original_module_id"] = module.get("module_id", "unknown")
        adapted["module_id"] = f"{module.get('module_id', 'unknown')}_{version}"
        adapted["adaptations_applied"] = []

        # Применяем гендерные адаптации в зависимости от типа
        if version == "masculine":
            adapted = self._apply_masculine_adaptations(adapted, module_type)
        elif version == "feminine":
            adapted = self._apply_feminine_adaptations(adapted, module_type)
        else:  # neutral
            adapted = self._apply_neutral_adaptations(adapted, module_type)

        # Валидация на стереотипы
        if self.deps.enable_stereotype_validation:
            adapted["stereotype_validation"] = self._validate_stereotypes(adapted)

        return adapted

    def _apply_masculine_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить маскулинные адаптации."""
        adaptations = []

        # Маскулинные паттерны коммуникации
        replacements = {
            "почувствуй": "осознай",
            "соединись с собой": "достигни понимания",
            "раскрой потенциал": "реализуй возможности",
            "гармония": "баланс",
            "забота о себе": "самоконтроль",
            "интуиция": "инсайт",
            "эмоциональный": "логический"
        }

        # Применяем замены к текстовым полям
        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': маскулинная адаптация")
                    module[key] = value

        module["adaptations_applied"] = adaptations
        module["adaptation_focus"] = "Логика, стратегия, достижение результата"

        return module

    def _apply_feminine_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить фемининные адаптации."""
        adaptations = []

        # Фемининные паттерны коммуникации
        replacements = {
            "достигни": "позволь себе достичь",
            "контролируй": "осознавай и направляй",
            "преодолей": "трансформируй",
            "эффективность": "гармоничность",
            "результат": "процесс роста",
            "логический": "интуитивный",
            "стратегия": "путь развития"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': фемининная адаптация")
                    module[key] = value

        module["adaptations_applied"] = adaptations
        module["adaptation_focus"] = "Эмоции, процесс, связь, рост"

        return module

    def _apply_neutral_adaptations(
        self,
        module: Dict[str, Any],
        module_type: str
    ) -> Dict[str, Any]:
        """Применить нейтральные адаптации."""
        adaptations = []

        # Нейтрализация языка
        replacements = {
            "он": "человек",
            "она": "человек",
            "мужчина": "человек",
            "женщина": "человек",
            "победа": "успех",
            "борьба": "процесс",
            "преодоление": "развитие"
        }

        for key, value in module.items():
            if isinstance(value, str):
                original = value
                for old, new in replacements.items():
                    if old in value.lower():
                        value = value.replace(old, new)
                if value != original:
                    adaptations.append(f"Поле '{key}': нейтрализация")
                    module[key] = value

        module["adaptations_applied"] = adaptations
        module["adaptation_focus"] = "Баланс, инклюзивность, универсальность"

        return module

    def _validate_stereotypes(self, module: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидировать модуль на отсутствие токсичных стереотипов.

        Args:
            module: Модуль для проверки

        Returns:
            Результаты валидации
        """
        text = str(module).lower()

        toxic_patterns = [
            "все мужчины", "все женщины", "типично мужской",
            "типично женский", "настоящий мужчина", "настоящая женщина",
            "мужчины должны", "женщины должны"
        ]

        issues = [pattern for pattern in toxic_patterns if pattern in text]

        return {
            "is_valid": len(issues) == 0,
            "issues_found": issues,
            "validated_at": "gender_adaptation_stage"
        }

    async def save_adapted_modules(
        self,
        adapted_modules: List[Dict[str, Any]],
        output_dir: str = "adapted_modules/gender"
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

        # Группируем по типу модуля
        modules_by_type = {}
        for module in adapted_modules:
            module_type = module.get("module_type", "unknown")
            if module_type not in modules_by_type:
                modules_by_type[module_type] = []
            modules_by_type[module_type].append(module)

        # Сохраняем каждый тип в отдельный файл
        saved_files = []
        for module_type, modules in modules_by_type.items():
            file_path = output_path / f"{module_type}_gender_adapted.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(modules, f, indent=2, ensure_ascii=False)
            saved_files.append(str(file_path))
            logger.info(f"Сохранено {len(modules)} модулей типа {module_type} в {file_path}")

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
            "multiplication_factor": 3,  # каждый модуль × 3 версии
            "gender_versions": self.deps.gender_versions,
            "stereotype_validation_enabled": self.deps.enable_stereotype_validation,
            "workflow_stage": "Step 4.1 - Gender Adaptation (Days 25-28)",
            "next_agent": "Pattern Age Adaptation Agent (Step 4.2)"
        }
