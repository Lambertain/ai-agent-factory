"""
Зависимости для Pattern Metaphor Weaver Agent.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ArchetypalImagesDatabase:
    """База архетипических образов."""

    def __post_init__(self):
        self.archetypes = {
            "hero": {
                "images": ["путник", "воин", "искатель"],
                "meaning": "Преодоление препятствий, трансформация через вызов",
                "therapeutic": "Активация ресурсного состояния, courage"
            },
            "wise_old_man": {
                "images": ["мудрец", "наставник", "старый дуб"],
                "meaning": "Внутренняя мудрость, guidance",
                "therapeutic": "Доступ к inner wisdom, решения"
            },
            "great_mother": {
                "images": ["земля", "океан", "древо жизни"],
                "meaning": "Забота, питание, безусловная любовь",
                "therapeutic": "Self-compassion, healing"
            }
        }


@dataclass
class MetaphorTemplatesDatabase:
    """База шаблонов метафор."""

    def __post_init__(self):
        self.templates = {
            "journey": {
                "structure": "Начало пути → Испытания → Трансформация → Возвращение",
                "examples": ["Герой пути", "Паломничество", "Восхождение на гору"]
            },
            "nature": {
                "structure": "Семя → Рост → Цветение → Плод",
                "examples": ["Река течет к океану", "Дерево сквозь времена года"]
            },
            "transformation": {
                "structure": "Старое состояние → Переход → Новое состояние",
                "examples": ["Гусеница и бабочка", "Феникс из пепла"]
            }
        }


@dataclass
class IsomorphicPatternsDatabase:
    """База изоморфных паттернов."""

    def __post_init__(self):
        self.patterns = {
            "stuck_pattern": {
                "metaphor": "Река, заблокированная плотиной",
                "mapping": {
                    "stuck_energy": "накопленная вода",
                    "resistance": "плотина",
                    "breakthrough": "прорыв воды"
                }
            }
        }


@dataclass
class PatternMetaphorWeaverDependencies:
    """Зависимости для Pattern Metaphor Weaver Agent."""

    api_key: str
    patternshift_project_path: str = ""
    user_id: Optional[str] = None
    program_id: Optional[str] = None

    archetypal_images_db: ArchetypalImagesDatabase = field(default_factory=ArchetypalImagesDatabase)
    metaphor_templates_db: MetaphorTemplatesDatabase = field(default_factory=MetaphorTemplatesDatabase)
    isomorphic_patterns_db: IsomorphicPatternsDatabase = field(default_factory=IsomorphicPatternsDatabase)


__all__ = ["PatternMetaphorWeaverDependencies"]
