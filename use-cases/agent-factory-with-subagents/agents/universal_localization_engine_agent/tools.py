# -*- coding: utf-8 -*-
"""
Инструменты для Universal Localization Engine Agent.

Комплексный набор инструментов для извлечения, перевода,
валидации и управления локализацией проектов.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass

from pydantic_ai import RunContext
from .dependencies import LocalizationEngineDependencies


@dataclass
class TranslationEntry:
    """Запись для перевода."""
    key: str
    source_text: str
    context: str = ""
    file_path: str = ""
    line_number: int = 0
    priority: str = "medium"  # low, medium, high, critical
    category: str = "general"  # ui, marketing, error, help, etc.


@dataclass
class LocaleData:
    """Данные локали."""
    locale: str
    translations: Dict[str, str]
    metadata: Dict[str, Any]
    coverage: float = 0.0
    quality_score: float = 0.0


# === ИЗВЛЕЧЕНИЕ КОНТЕНТА ===

async def extract_translatable_content(
    ctx: RunContext[LocalizationEngineDependencies],
    project_path: str,
    extraction_config: Dict[str, Any] = None
) -> str:
    """
    Извлечение всего переводимого контента из проекта.

    Args:
        ctx: Контекст выполнения
        project_path: Путь к проекту
        extraction_config: Конфигурация извлечения

    Returns:
        JSON с извлеченным контентом
    """
    if extraction_config is None:
        extraction_config = {
            "file_patterns": ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx", "**/*.vue"],
            "extract_methods": ["t", "i18n", "translate", "$t", "_"],
            "extract_attributes": ["title", "alt", "placeholder", "aria-label"],
            "extract_comments": True,
            "exclude_patterns": ["node_modules", "test", ".git", "dist", "build"]
        }

    deps = ctx.deps

    try:
        # Поиск файлов для сканирования
        project_dir = Path(project_path)
        if not project_dir.exists():
            return json.dumps({"error": f"Проект не найден: {project_path}"})

        found_entries = []
        processed_files = 0

        # Сканирование файлов
        for pattern in extraction_config["file_patterns"]:
            for file_path in project_dir.glob(pattern):
                # Проверка исключений
                if any(excl in str(file_path) for excl in extraction_config["exclude_patterns"]):
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    file_entries = await _extract_from_file(
                        file_path, content, extraction_config
                    )
                    found_entries.extend(file_entries)
                    processed_files += 1

                except Exception as e:
                    continue

        # Анализ и приоритизация найденного контента
        analyzed_entries = await _analyze_extraction_results(found_entries, deps)

        # Группировка по категориям
        categorized_content = await _categorize_content(analyzed_entries, deps)

        result = {
            "extraction_summary": {
                "total_files_processed": processed_files,
                "total_strings_found": len(found_entries),
                "unique_strings": len(set(entry.source_text for entry in found_entries)),
                "categories": list(categorized_content.keys()),
                "project_path": project_path
            },
            "content_by_category": categorized_content,
            "extraction_recommendations": await _generate_extraction_recommendations(
                found_entries, deps
            ),
            "localization_structure_suggestion": await _suggest_localization_structure(
                found_entries, deps
            )
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Ошибка извлечения контента: {str(e)}"})


async def _extract_from_file(
    file_path: Path,
    content: str,
    config: Dict[str, Any]
) -> List[TranslationEntry]:
    """Извлечение переводимого контента из отдельного файла."""

    entries = []
    lines = content.split('\n')

    # Паттерны для извлечения
    method_patterns = []
    for method in config["extract_methods"]:
        # t('text'), i18n("text"), etc.
        method_patterns.append(rf'{method}\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)')

    attr_patterns = []
    for attr in config["extract_attributes"]:
        # title="text", alt="text", etc.
        attr_patterns.append(rf'{attr}\s*=\s*[\'"]([^\'"]+)[\'"]')

    # Поиск по всем паттернам
    for line_num, line in enumerate(lines, 1):
        # Методы перевода
        for pattern in method_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                text = match.group(1)
                if len(text.strip()) > 0:
                    entries.append(TranslationEntry(
                        key=_generate_key(text),
                        source_text=text,
                        context=_extract_context(lines, line_num),
                        file_path=str(file_path),
                        line_number=line_num,
                        category="ui"
                    ))

        # HTML атрибуты
        for pattern in attr_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                text = match.group(1)
                if len(text.strip()) > 0:
                    entries.append(TranslationEntry(
                        key=_generate_key(text),
                        source_text=text,
                        context=_extract_context(lines, line_num),
                        file_path=str(file_path),
                        line_number=line_num,
                        category="accessibility"
                    ))

        # Комментарии с TODO: translate, FIXME: i18n, etc.
        if config["extract_comments"]:
            comment_match = re.search(r'//.*(?:translate|i18n|localize).*[\'"]([^\'"]+)[\'"]', line, re.IGNORECASE)
            if comment_match:
                text = comment_match.group(1)
                entries.append(TranslationEntry(
                    key=_generate_key(text),
                    source_text=text,
                    context="From comment: " + line.strip(),
                    file_path=str(file_path),
                    line_number=line_num,
                    category="todo"
                ))

    return entries


def _generate_key(text: str) -> str:
    """Генерация ключа для переводимого текста."""
    # Простая генерация ключа из текста
    key = re.sub(r'[^\w\s]', '', text.lower())
    key = re.sub(r'\s+', '_', key.strip())
    return key[:50]  # Ограничиваем длину


def _extract_context(lines: List[str], line_num: int) -> str:
    """Извлечение контекста вокруг найденной строки."""
    context_lines = []
    start = max(0, line_num - 3)
    end = min(len(lines), line_num + 2)

    for i in range(start, end):
        prefix = ">>> " if i + 1 == line_num else "    "
        context_lines.append(f"{prefix}{lines[i].strip()}")

    return "\n".join(context_lines)


async def _analyze_extraction_results(
    entries: List[TranslationEntry],
    deps: LocalizationEngineDependencies
) -> List[TranslationEntry]:
    """Анализ и приоритизация извлеченного контента."""

    # Определение приоритетов на основе контекста
    for entry in entries:
        # Высокий приоритет для ошибок и уведомлений
        if any(word in entry.source_text.lower() for word in ['error', 'warning', 'success', 'fail']):
            entry.priority = "high"
            entry.category = "messages"

        # Критический приоритет для безопасности
        elif any(word in entry.source_text.lower() for word in ['password', 'security', 'login', 'auth']):
            entry.priority = "critical"
            entry.category = "security"

        # Низкий приоритет для отладочной информации
        elif any(word in entry.source_text.lower() for word in ['debug', 'console', 'log']):
            entry.priority = "low"
            entry.category = "debug"

        # Высокий приоритет для пользовательских действий
        elif any(word in entry.source_text.lower() for word in ['button', 'click', 'submit', 'save']):
            entry.priority = "high"
            entry.category = "actions"

    return entries


async def _categorize_content(
    entries: List[TranslationEntry],
    deps: LocalizationEngineDependencies
) -> Dict[str, List[Dict[str, Any]]]:
    """Группировка контента по категориям."""

    categories = {}

    for entry in entries:
        if entry.category not in categories:
            categories[entry.category] = []

        categories[entry.category].append({
            "key": entry.key,
            "text": entry.source_text,
            "context": entry.context,
            "file": entry.file_path,
            "line": entry.line_number,
            "priority": entry.priority
        })

    # Сортировка по приоритету
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    for category in categories:
        categories[category].sort(key=lambda x: priority_order.get(x["priority"], 2))

    return categories


async def _generate_extraction_recommendations(
    entries: List[TranslationEntry],
    deps: LocalizationEngineDependencies
) -> List[str]:
    """Генерация рекомендаций по извлеченному контенту."""

    recommendations = []

    # Анализ качества извлечения
    total_entries = len(entries)
    unique_texts = len(set(entry.source_text for entry in entries))

    if total_entries > 0:
        duplicate_ratio = 1 - (unique_texts / total_entries)
        if duplicate_ratio > 0.3:
            recommendations.append(
                f"Обнаружено {duplicate_ratio:.1%} дублирующихся строк. "
                "Рекомендуется создать переиспользуемые ключи перевода."
            )

    # Анализ длины строк
    long_strings = [e for e in entries if len(e.source_text) > 100]
    if long_strings:
        recommendations.append(
            f"Найдено {len(long_strings)} длинных строк (>100 символов). "
            "Рекомендуется разбить их на более короткие фрагменты."
        )

    # Анализ структуры ключей
    if deps.localization_structure == "flat":
        recommendations.append(
            "Рекомендуется использовать иерархическую структуру ключей "
            "для лучшей организации переводов."
        )

    # Проверка покрытия контента
    files_with_content = len(set(entry.file_path for entry in entries))
    if files_with_content < 5:
        recommendations.append(
            "Низкое покрытие файлов с переводимым контентом. "
            "Проверьте настройки извлечения и паттерны поиска."
        )

    return recommendations


async def _suggest_localization_structure(
    entries: List[TranslationEntry],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Предложение структуры организации локализации."""

    # Анализ категорий контента
    categories = {}
    for entry in entries:
        if entry.category not in categories:
            categories[entry.category] = 0
        categories[entry.category] += 1

    # Рекомендуемая структура файлов
    structure = {
        "format": "json",  # json, yaml, po
        "organization": "namespace",  # flat, namespace, feature-based
        "suggested_files": {},
        "naming_convention": "kebab-case"
    }

    # Предложение файлов на основе категорий
    for category, count in categories.items():
        if count > 10:  # Много строк - отдельный файл
            structure["suggested_files"][f"{category}.json"] = {
                "description": f"Переводы для категории '{category}'",
                "estimated_strings": count
            }

    # Общие рекомендации
    if len(categories) > 5:
        structure["organization"] = "feature-based"
        structure["note"] = "Рекомендуется организация по функциональным модулям"

    return structure


# === ПЕРЕВОД КОНТЕНТА ===

async def translate_content_batch(
    ctx: RunContext[LocalizationEngineDependencies],
    content_data: Dict[str, Any],
    target_languages: List[str],
    translation_config: Dict[str, Any] = None
) -> str:
    """
    Массовый перевод контента на несколько языков.

    Args:
        ctx: Контекст выполнения
        content_data: Данные для перевода
        target_languages: Целевые языки
        translation_config: Конфигурация перевода

    Returns:
        JSON с переведенным контентом
    """
    if translation_config is None:
        translation_config = {
            "quality": "professional",
            "preserve_formatting": True,
            "context_aware": True,
            "batch_size": 50
        }

    deps = ctx.deps

    try:
        # Подготовка данных для перевода
        translation_batches = await _prepare_translation_batches(
            content_data, translation_config["batch_size"]
        )

        # Результаты перевода по языкам
        translated_results = {}

        for target_lang in target_languages:
            print(f"Переводим на {target_lang}...")
            translated_results[target_lang] = {}

            for batch_name, batch_content in translation_batches.items():
                batch_result = await _translate_batch(
                    batch_content, target_lang, translation_config, deps
                )
                translated_results[target_lang][batch_name] = batch_result

        # Постобработка и валидация
        validated_results = await _validate_batch_translations(
            translated_results, content_data, deps
        )

        # Генерация отчета о переводе
        translation_report = await _generate_translation_report(
            translated_results, target_languages, deps
        )

        result = {
            "translation_results": validated_results,
            "translation_report": translation_report,
            "quality_metrics": await _calculate_translation_metrics(
                validated_results, deps
            ),
            "recommendations": await _generate_translation_recommendations(
                validated_results, deps
            )
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Ошибка массового перевода: {str(e)}"})


async def _prepare_translation_batches(
    content_data: Dict[str, Any],
    batch_size: int
) -> Dict[str, List[Dict[str, Any]]]:
    """Подготовка данных для batch перевода."""

    batches = {}
    current_batch = []
    batch_count = 0

    # Обработка контента по категориям
    for category, items in content_data.get("content_by_category", {}).items():
        for item in items:
            current_batch.append({
                "key": item["key"],
                "text": item["text"],
                "context": item.get("context", ""),
                "category": category,
                "priority": item.get("priority", "medium")
            })

            if len(current_batch) >= batch_size:
                batches[f"batch_{batch_count}"] = current_batch
                current_batch = []
                batch_count += 1

    # Добавляем последний batch если есть данные
    if current_batch:
        batches[f"batch_{batch_count}"] = current_batch

    return batches


async def _translate_batch(
    batch_content: List[Dict[str, Any]],
    target_language: str,
    config: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, str]:
    """Перевод одного batch контента."""

    # Формирование промпта для перевода
    translation_prompt = f"""
Переведи следующий контент на {target_language}.

ТРЕБОВАНИЯ:
- Качество: {config['quality']}
- Сохраняй форматирование: {config['preserve_formatting']}
- Учитывай контекст: {config['context_aware']}
- Домен проекта: {deps.domain_type}
- Тип проекта: {deps.project_type}

КОНТЕНТ ДЛЯ ПЕРЕВОДА:
"""

    for item in batch_content:
        translation_prompt += f"""
Ключ: {item['key']}
Текст: "{item['text']}"
Категория: {item['category']}
Контекст: {item['context']}
---
"""

    translation_prompt += """
ВАЖНО:
1. Переводи точно, сохраняя смысл и тон
2. Адаптируй под культурные особенности
3. Сохраняй технические термины при необходимости
4. Возвращай результат в формате JSON: {"key": "перевод"}
"""

    # Здесь был бы вызов LLM для перевода
    # Для демонстрации возвращаем заглушку
    translated = {}
    for item in batch_content:
        # Заглушка - в реальности здесь вызов модели
        translated[item["key"]] = f"[{target_language}] {item['text']}"

    return translated


async def _validate_batch_translations(
    translations: Dict[str, Any],
    original_content: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Валидация результатов batch перевода."""

    validated = {}

    for language, lang_translations in translations.items():
        validated[language] = {}
        validation_issues = []

        for batch_name, batch_translations in lang_translations.items():
            validated_batch = {}

            for key, translation in batch_translations.items():
                # Базовая валидация
                if not translation or len(translation.strip()) == 0:
                    validation_issues.append(f"Пустой перевод для ключа: {key}")
                    continue

                # Проверка длины (не более чем в 2 раза больше оригинала)
                original_text = _find_original_text(key, original_content)
                if original_text and len(translation) > len(original_text) * 2:
                    validation_issues.append(f"Слишком длинный перевод для ключа: {key}")

                validated_batch[key] = translation

            validated[language][batch_name] = validated_batch

        # Добавляем информацию о проблемах валидации
        if validation_issues:
            validated[language]["validation_issues"] = validation_issues

    return validated


def _find_original_text(key: str, content_data: Dict[str, Any]) -> Optional[str]:
    """Поиск оригинального текста по ключу."""
    for category, items in content_data.get("content_by_category", {}).items():
        for item in items:
            if item["key"] == key:
                return item["text"]
    return None


async def _generate_translation_report(
    translations: Dict[str, Any],
    target_languages: List[str],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Генерация отчета о переводе."""

    report = {
        "summary": {
            "target_languages": target_languages,
            "total_languages": len(target_languages),
            "total_translations": 0,
            "completion_status": {}
        },
        "language_statistics": {},
        "quality_indicators": {}
    }

    for language in target_languages:
        lang_data = translations.get(language, {})
        lang_translations = 0

        # Подсчет переводов
        for batch_name, batch_data in lang_data.items():
            if batch_name != "validation_issues":
                lang_translations += len(batch_data)

        report["language_statistics"][language] = {
            "translations_count": lang_translations,
            "validation_issues": len(lang_data.get("validation_issues", [])),
            "completion_rate": "100%" if lang_translations > 0 else "0%"
        }

        report["summary"]["total_translations"] += lang_translations

    return report


async def _calculate_translation_metrics(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Расчет метрик качества перевода."""

    metrics = {
        "coverage": {},
        "quality_scores": {},
        "consistency": {},
        "performance": {}
    }

    for language, lang_data in translations.items():
        total_strings = 0
        translated_strings = 0
        issues_count = 0

        for batch_name, batch_data in lang_data.items():
            if batch_name == "validation_issues":
                issues_count = len(batch_data)
            else:
                batch_size = len(batch_data)
                total_strings += batch_size
                translated_strings += batch_size

        # Метрики покрытия
        coverage = (translated_strings / total_strings * 100) if total_strings > 0 else 0
        metrics["coverage"][language] = f"{coverage:.1f}%"

        # Оценка качества (базовая)
        quality_score = max(0, 100 - (issues_count * 10))
        metrics["quality_scores"][language] = f"{quality_score}/100"

    return metrics


async def _generate_translation_recommendations(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> List[str]:
    """Генерация рекомендаций по переводам."""

    recommendations = []

    # Анализ качества по языкам
    for language, lang_data in translations.items():
        issues = lang_data.get("validation_issues", [])
        if issues:
            recommendations.append(
                f"Язык {language}: найдено {len(issues)} проблем валидации. "
                "Рекомендуется ручная проверка."
            )

    # Общие рекомендации
    if len(translations) > 5:
        recommendations.append(
            "При большом количестве языков рекомендуется "
            "постепенное развертывание и мониторинг качества."
        )

    if deps.enable_cultural_adaptation:
        recommendations.append(
            "Включена культурная адаптация. Рекомендуется проверка "
            "локальных экспертов для ключевых рынков."
        )

    return recommendations


# === ВАЛИДАЦИЯ КАЧЕСТВА ===

async def validate_translation_quality(
    ctx: RunContext[LocalizationEngineDependencies],
    translations: Dict[str, Any],
    validation_config: Dict[str, Any] = None
) -> str:
    """
    Комплексная валидация качества переводов.

    Args:
        ctx: Контекст выполнения
        translations: Переводы для валидации
        validation_config: Конфигурация валидации

    Returns:
        JSON с результатами валидации
    """
    if validation_config is None:
        validation_config = {
            "check_completeness": True,
            "check_consistency": True,
            "check_grammar": True,
            "check_formatting": True,
            "check_length": True,
            "check_cultural": True
        }

    deps = ctx.deps

    try:
        validation_results = {}

        for language, lang_translations in translations.items():
            print(f"Валидация переводов для {language}...")

            lang_results = {
                "completeness": {},
                "consistency": {},
                "grammar": {},
                "formatting": {},
                "length": {},
                "cultural": {},
                "overall_score": 0
            }

            # Проверка полноты
            if validation_config["check_completeness"]:
                lang_results["completeness"] = await _check_completeness(
                    lang_translations, deps
                )

            # Проверка консистентности
            if validation_config["check_consistency"]:
                lang_results["consistency"] = await _check_consistency(
                    lang_translations, deps
                )

            # Проверка грамматики
            if validation_config["check_grammar"]:
                lang_results["grammar"] = await _check_grammar(
                    lang_translations, language, deps
                )

            # Проверка форматирования
            if validation_config["check_formatting"]:
                lang_results["formatting"] = await _check_formatting(
                    lang_translations, deps
                )

            # Проверка длины
            if validation_config["check_length"]:
                lang_results["length"] = await _check_length(
                    lang_translations, deps
                )

            # Культурная проверка
            if validation_config["check_cultural"]:
                lang_results["cultural"] = await _check_cultural_appropriateness(
                    lang_translations, language, deps
                )

            # Расчет общего балла
            lang_results["overall_score"] = await _calculate_overall_score(
                lang_results
            )

            validation_results[language] = lang_results

        # Генерация итогового отчета
        summary = await _generate_validation_summary(validation_results)

        result = {
            "validation_results": validation_results,
            "summary": summary,
            "recommendations": await _generate_quality_recommendations(
                validation_results, deps
            ),
            "next_steps": await _suggest_next_steps(validation_results, deps)
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Ошибка валидации качества: {str(e)}"})


async def _check_completeness(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка полноты переводов."""

    total_keys = 0
    translated_keys = 0
    missing_keys = []

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            total_keys += 1
            if translation and len(translation.strip()) > 0:
                translated_keys += 1
            else:
                missing_keys.append(key)

    completeness_rate = (translated_keys / total_keys * 100) if total_keys > 0 else 0

    return {
        "completeness_rate": f"{completeness_rate:.1f}%",
        "total_keys": total_keys,
        "translated_keys": translated_keys,
        "missing_keys": missing_keys[:10],  # Первые 10 для примера
        "score": min(100, completeness_rate)
    }


async def _check_consistency(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка консистентности переводов."""

    # Поиск повторяющихся терминов
    term_translations = {}
    inconsistencies = []

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            # Извлекаем ключевые термины
            terms = _extract_key_terms(translation)
            for term in terms:
                if term not in term_translations:
                    term_translations[term] = []
                term_translations[term].append((key, translation))

    # Поиск несоответствий
    for term, occurrences in term_translations.items():
        if len(occurrences) > 1:
            translations_set = set(occ[1] for occ in occurrences)
            if len(translations_set) > 1:
                inconsistencies.append({
                    "term": term,
                    "variations": list(translations_set),
                    "occurrences": len(occurrences)
                })

    consistency_score = max(0, 100 - len(inconsistencies) * 5)

    return {
        "consistency_score": consistency_score,
        "total_terms": len(term_translations),
        "inconsistent_terms": len(inconsistencies),
        "inconsistencies": inconsistencies[:5],  # Первые 5
        "score": consistency_score
    }


def _extract_key_terms(text: str) -> List[str]:
    """Извлечение ключевых терминов из текста."""
    # Простая логика извлечения терминов
    words = re.findall(r'\b\w{3,}\b', text.lower())
    # Исключаем общие слова
    common_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'have', 'from'}
    return [word for word in words if word not in common_words]


async def _check_grammar(
    translations: Dict[str, Any],
    language: str,
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка грамматики переводов."""

    # Базовая проверка грамматики
    grammar_issues = []
    total_checked = 0

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            total_checked += 1

            # Простые проверки
            issues = _basic_grammar_check(translation, language)
            if issues:
                grammar_issues.extend([
                    {"key": key, "translation": translation, "issue": issue}
                    for issue in issues
                ])

    grammar_score = max(0, 100 - len(grammar_issues) * 3)

    return {
        "grammar_score": grammar_score,
        "total_checked": total_checked,
        "issues_found": len(grammar_issues),
        "issues": grammar_issues[:5],  # Первые 5
        "score": grammar_score
    }


def _basic_grammar_check(text: str, language: str) -> List[str]:
    """Базовая проверка грамматики."""
    issues = []

    # Общие проверки
    if text.count('(') != text.count(')'):
        issues.append("Несбалансированные скобки")

    if text.count('"') % 2 != 0:
        issues.append("Несбалансированные кавычки")

    # Проверка начала и конца предложений
    if len(text) > 1:
        if text[0].islower() and text.endswith('.'):
            issues.append("Предложение начинается с маленькой буквы")

    return issues


async def _check_formatting(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка форматирования переводов."""

    formatting_issues = []
    total_checked = 0

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            total_checked += 1

            # Проверки форматирования
            issues = _check_text_formatting(translation)
            if issues:
                formatting_issues.extend([
                    {"key": key, "translation": translation, "issue": issue}
                    for issue in issues
                ])

    formatting_score = max(0, 100 - len(formatting_issues) * 2)

    return {
        "formatting_score": formatting_score,
        "total_checked": total_checked,
        "issues_found": len(formatting_issues),
        "issues": formatting_issues[:5],
        "score": formatting_score
    }


def _check_text_formatting(text: str) -> List[str]:
    """Проверка форматирования текста."""
    issues = []

    # Проверка пробелов
    if text.startswith(' ') or text.endswith(' '):
        issues.append("Лишние пробелы в начале или конце")

    # Проверка двойных пробелов
    if '  ' in text:
        issues.append("Двойные пробелы")

    # Проверка переносов строк
    if '\n' in text and not text.strip().endswith('\n'):
        issues.append("Некорректные переносы строк")

    return issues


async def _check_length(
    translations: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка длины переводов."""

    length_issues = []
    total_checked = 0
    avg_expansion = 0

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            total_checked += 1

            # Предполагаем, что оригинал в среднем на 20% короче
            estimated_original_length = len(translation) * 0.8
            expansion_rate = len(translation) / estimated_original_length if estimated_original_length > 0 else 1

            if expansion_rate > 2.0:  # Более чем в 2 раза длиннее
                length_issues.append({
                    "key": key,
                    "translation": translation[:50] + "...",
                    "length": len(translation),
                    "expansion_rate": f"{expansion_rate:.1f}x"
                })

            avg_expansion += expansion_rate

    avg_expansion = avg_expansion / total_checked if total_checked > 0 else 1
    length_score = max(0, 100 - len(length_issues) * 5)

    return {
        "length_score": length_score,
        "average_expansion": f"{avg_expansion:.1f}x",
        "long_translations": len(length_issues),
        "issues": length_issues[:5],
        "score": length_score
    }


async def _check_cultural_appropriateness(
    translations: Dict[str, Any],
    language: str,
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Проверка культурной адекватности."""

    cultural_issues = []
    total_checked = 0

    # Базовые культурные проверки
    cultural_markers = _get_cultural_markers(language)

    for batch_name, batch_data in translations.items():
        if batch_name == "validation_issues":
            continue

        for key, translation in batch_data.items():
            total_checked += 1

            # Проверка культурных маркеров
            issues = _check_cultural_markers(translation, cultural_markers)
            if issues:
                cultural_issues.extend([
                    {"key": key, "translation": translation, "issue": issue}
                    for issue in issues
                ])

    cultural_score = max(0, 100 - len(cultural_issues) * 4)

    return {
        "cultural_score": cultural_score,
        "total_checked": total_checked,
        "cultural_issues": len(cultural_issues),
        "issues": cultural_issues[:3],
        "score": cultural_score
    }


def _get_cultural_markers(language: str) -> Dict[str, Any]:
    """Получение культурных маркеров для языка."""
    markers = {
        "ru": {
            "formal_pronouns": ["Вы", "Ваш"],
            "informal_pronouns": ["ты", "твой"],
            "sensitive_topics": ["политика", "религия"]
        },
        "de": {
            "formal_pronouns": ["Sie", "Ihr"],
            "informal_pronouns": ["du", "dein"],
            "compound_words": True
        },
        "ja": {
            "honorifics": ["さん", "様", "君"],
            "formal_forms": ["です", "ます"],
            "hierarchical": True
        }
    }
    return markers.get(language, {})


def _check_cultural_markers(text: str, markers: Dict[str, Any]) -> List[str]:
    """Проверка культурных маркеров в тексте."""
    issues = []

    # Проверка формальности
    if "formal_pronouns" in markers and "informal_pronouns" in markers:
        has_formal = any(pronoun in text for pronoun in markers["formal_pronouns"])
        has_informal = any(pronoun in text for pronoun in markers["informal_pronouns"])

        if has_formal and has_informal:
            issues.append("Смешение формального и неформального стиля")

    return issues


async def _calculate_overall_score(results: Dict[str, Any]) -> float:
    """Расчет общего балла качества."""
    scores = []

    for check_type, check_results in results.items():
        if isinstance(check_results, dict) and "score" in check_results:
            scores.append(check_results["score"])

    return sum(scores) / len(scores) if scores else 0


async def _generate_validation_summary(
    validation_results: Dict[str, Any]
) -> Dict[str, Any]:
    """Генерация итогового отчета валидации."""

    summary = {
        "overall_quality": 0,
        "language_scores": {},
        "critical_issues": [],
        "recommendations": []
    }

    total_score = 0
    language_count = 0

    for language, lang_results in validation_results.items():
        lang_score = lang_results.get("overall_score", 0)
        summary["language_scores"][language] = f"{lang_score:.1f}/100"

        total_score += lang_score
        language_count += 1

        # Сбор критических проблем
        for check_type, check_results in lang_results.items():
            if isinstance(check_results, dict) and check_results.get("score", 100) < 70:
                summary["critical_issues"].append(f"{language}: {check_type}")

    summary["overall_quality"] = total_score / language_count if language_count > 0 else 0

    return summary


async def _generate_quality_recommendations(
    validation_results: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> List[str]:
    """Генерация рекомендаций по качеству."""

    recommendations = []

    for language, lang_results in validation_results.items():
        # Рекомендации по полноте
        completeness = lang_results.get("completeness", {})
        if completeness.get("score", 100) < 95:
            recommendations.append(
                f"{language}: Завершить недостающие переводы "
                f"({100 - completeness.get('score', 100):.0f}% неполных)"
            )

        # Рекомендации по консистентности
        consistency = lang_results.get("consistency", {})
        if consistency.get("score", 100) < 80:
            recommendations.append(
                f"{language}: Стандартизировать терминологию "
                f"({consistency.get('inconsistent_terms', 0)} несогласованных терминов)"
            )

        # Рекомендации по грамматике
        grammar = lang_results.get("grammar", {})
        if grammar.get("score", 100) < 85:
            recommendations.append(
                f"{language}: Исправить грамматические ошибки "
                f"({grammar.get('issues_found', 0)} проблем)"
            )

    return recommendations


async def _suggest_next_steps(
    validation_results: Dict[str, Any],
    deps: LocalizationEngineDependencies
) -> List[str]:
    """Предложение следующих шагов."""

    steps = []

    # Анализ общего качества
    avg_quality = sum(
        lang_results.get("overall_score", 0)
        for lang_results in validation_results.values()
    ) / len(validation_results) if validation_results else 0

    if avg_quality < 70:
        steps.append("1. Критический пересмотр переводов с привлечением экспертов")
    elif avg_quality < 85:
        steps.append("1. Исправление выявленных проблем качества")
    else:
        steps.append("1. Финальная проверка и подготовка к развертыванию")

    if deps.enable_cultural_adaptation:
        steps.append("2. Дополнительная культурная валидация с носителями языка")

    steps.append("3. Тестирование в реальной среде с ограниченной аудиторией")
    steps.append("4. Создание процедур для обновления переводов")

    return steps


# === ГЕНЕРАЦИЯ ФАЙЛОВ ЛОКАЛИ ===

async def generate_locale_files(
    ctx: RunContext[LocalizationEngineDependencies],
    translations: Dict[str, Any],
    output_format: str = "json",
    file_structure: str = "namespace"
) -> str:
    """
    Генерация файлов локализации в различных форматах.

    Args:
        ctx: Контекст выполнения
        translations: Переводы
        output_format: Формат вывода (json, yaml, po, xliff)
        file_structure: Структура файлов (flat, namespace, feature-based)

    Returns:
        JSON с информацией о созданных файлах
    """
    deps = ctx.deps

    try:
        generated_files = []
        output_path = Path(deps.project_path) / "locales"
        output_path.mkdir(parents=True, exist_ok=True)

        for language, lang_translations in translations.items():
            if language == "validation_issues":
                continue

            # Подготовка данных для файла
            file_data = await _prepare_locale_file_data(
                lang_translations, file_structure
            )

            # Генерация файла в нужном формате
            filename = await _generate_locale_file(
                language, file_data, output_format, output_path, file_structure
            )

            if filename:
                generated_files.append({
                    "language": language,
                    "filename": filename,
                    "format": output_format,
                    "structure": file_structure,
                    "size": _get_file_size(output_path / filename),
                    "entries_count": _count_translation_entries(file_data)
                })

        # Генерация индексного файла
        index_file = await _generate_locale_index(
            generated_files, output_path, output_format
        )

        result = {
            "generated_files": generated_files,
            "index_file": index_file,
            "output_directory": str(output_path),
            "total_files": len(generated_files),
            "format": output_format,
            "structure": file_structure,
            "usage_instructions": await _generate_usage_instructions(
                output_format, file_structure, deps
            )
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Ошибка генерации файлов локали: {str(e)}"})


async def _prepare_locale_file_data(
    translations: Dict[str, Any],
    structure: str
) -> Dict[str, Any]:
    """Подготовка данных для файла локали."""

    if structure == "flat":
        # Плоская структура: все ключи на одном уровне
        flat_data = {}
        for batch_name, batch_data in translations.items():
            if batch_name != "validation_issues":
                flat_data.update(batch_data)
        return flat_data

    elif structure == "namespace":
        # Пространства имен: группировка по категориям
        namespaced_data = {}
        for batch_name, batch_data in translations.items():
            if batch_name != "validation_issues":
                # Создаем namespace из имени batch
                namespace = batch_name.replace("batch_", "section_")
                namespaced_data[namespace] = batch_data
        return namespaced_data

    elif structure == "feature-based":
        # Группировка по функциональным модулям
        feature_data = {
            "common": {},
            "ui": {},
            "messages": {},
            "errors": {},
            "navigation": {}
        }

        for batch_name, batch_data in translations.items():
            if batch_name != "validation_issues":
                # Простая логика определения категории
                for key, value in batch_data.items():
                    if "error" in key.lower():
                        feature_data["errors"][key] = value
                    elif "nav" in key.lower() or "menu" in key.lower():
                        feature_data["navigation"][key] = value
                    elif "button" in key.lower() or "label" in key.lower():
                        feature_data["ui"][key] = value
                    elif "message" in key.lower() or "notify" in key.lower():
                        feature_data["messages"][key] = value
                    else:
                        feature_data["common"][key] = value

        return feature_data

    else:
        # По умолчанию - namespace
        return await _prepare_locale_file_data(translations, "namespace")


async def _generate_locale_file(
    language: str,
    data: Dict[str, Any],
    format_type: str,
    output_path: Path,
    structure: str
) -> Optional[str]:
    """Генерация файла локали в нужном формате."""

    filename = f"{language}.{format_type}"
    file_path = output_path / filename

    try:
        if format_type == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        elif format_type == "yaml":
            import yaml
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        elif format_type == "po":
            content = _convert_to_po_format(data, language)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        else:
            # По умолчанию JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        return filename

    except Exception as e:
        print(f"Ошибка создания файла {filename}: {e}")
        return None


def _convert_to_po_format(data: Dict[str, Any], language: str) -> str:
    """Конвертация данных в формат PO (GNU gettext)."""

    po_content = f'''# Translation file for {language}
# Generated by Universal Localization Engine Agent
msgid ""
msgstr ""
"Language: {language}\\n"
"Content-Type: text/plain; charset=UTF-8\\n"

'''

    def _write_po_entries(entries, prefix=""):
        content = ""
        for key, value in entries.items():
            if isinstance(value, dict):
                content += _write_po_entries(value, f"{prefix}{key}.")
            else:
                full_key = f"{prefix}{key}"
                content += f'msgid "{full_key}"\n'
                content += f'msgstr "{value}"\n\n'
        return content

    po_content += _write_po_entries(data)
    return po_content


def _get_file_size(file_path: Path) -> str:
    """Получение размера файла в читаемом формате."""
    try:
        size = file_path.stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "Unknown"


def _count_translation_entries(data: Dict[str, Any]) -> int:
    """Подсчет количества записей перевода."""
    count = 0

    def _count_recursive(obj):
        nonlocal count
        if isinstance(obj, dict):
            for value in obj.values():
                if isinstance(value, dict):
                    _count_recursive(value)
                else:
                    count += 1

    _count_recursive(data)
    return count


async def _generate_locale_index(
    files: List[Dict[str, Any]],
    output_path: Path,
    format_type: str
) -> str:
    """Генерация индексного файла для локалей."""

    index_data = {
        "locales": {},
        "metadata": {
            "generated_at": "2024-01-01T00:00:00Z",  # В реальности текущая дата
            "total_locales": len(files),
            "format": format_type,
            "generator": "Universal Localization Engine Agent"
        }
    }

    for file_info in files:
        index_data["locales"][file_info["language"]] = {
            "file": file_info["filename"],
            "entries": file_info["entries_count"],
            "size": file_info["size"]
        }

    index_filename = f"index.{format_type}"
    index_path = output_path / index_filename

    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    return index_filename


async def _generate_usage_instructions(
    format_type: str,
    structure: str,
    deps: LocalizationEngineDependencies
) -> Dict[str, Any]:
    """Генерация инструкций по использованию."""

    instructions = {
        "format": format_type,
        "structure": structure,
        "integration_examples": {},
        "best_practices": []
    }

    # Примеры интеграции для разных фреймворков
    if deps.framework == "react":
        instructions["integration_examples"]["react"] = {
            "library": "react-i18next",
            "setup": "npm install react-i18next i18next",
            "usage": "const { t } = useTranslation(); return <div>{t('key')}</div>;"
        }

    elif deps.framework == "vue":
        instructions["integration_examples"]["vue"] = {
            "library": "vue-i18n",
            "setup": "npm install vue-i18n",
            "usage": "<template>{{ $t('key') }}</template>"
        }

    # Лучшие практики
    instructions["best_practices"] = [
        f"Используйте {structure} структуру для лучшей организации",
        f"Загружайте {format_type} файлы асинхронно для оптимизации",
        "Кэшируйте переводы для улучшения производительности",
        "Реализуйте fallback на базовый язык",
        "Регулярно обновляйте переводы через CI/CD"
    ]

    return instructions


# Остальные инструменты будут добавлены в следующих частях...

async def analyze_localization_coverage(
    ctx: RunContext[LocalizationEngineDependencies],
    project_path: str,
    current_translations: Dict[str, Any] = None
) -> str:
    """Анализ покрытия локализации проекта."""
    # Заглушка для инструмента
    return json.dumps({"message": "Анализ покрытия локализации"})


async def optimize_translation_workflow(
    ctx: RunContext[LocalizationEngineDependencies],
    workflow_config: Dict[str, Any]
) -> str:
    """Оптимизация workflow локализации."""
    return json.dumps({"message": "Оптимизация workflow"})


async def create_translation_memory(
    ctx: RunContext[LocalizationEngineDependencies],
    historical_data: Dict[str, Any]
) -> str:
    """Создание памяти переводов."""
    return json.dumps({"message": "Создание памяти переводов"})


async def validate_ui_compatibility(
    ctx: RunContext[LocalizationEngineDependencies],
    translations: Dict[str, Any],
    ui_constraints: Dict[str, Any]
) -> str:
    """Валидация совместимости с UI."""
    return json.dumps({"message": "Валидация UI совместимости"})


async def generate_cultural_adaptation(
    ctx: RunContext[LocalizationEngineDependencies],
    content: Dict[str, Any],
    target_locales: List[str]
) -> str:
    """Генерация культурной адаптации."""
    return json.dumps({"message": "Культурная адаптация"})


async def manage_translation_projects(
    ctx: RunContext[LocalizationEngineDependencies],
    action: str,
    project_data: Dict[str, Any] = None
) -> str:
    """Управление проектами локализации."""
    return json.dumps({"message": f"Управление проектами: {action}"})