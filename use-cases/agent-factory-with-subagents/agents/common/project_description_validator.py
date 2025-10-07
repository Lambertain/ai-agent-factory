"""
Валидатор полноты описания проекта в Archon.

Проверяет наличие обязательных полей в описании проекта перед началом работы.
Если описание неполное, предлагает интерактивный диалог для его создания.

Автор: Archon Implementation Engineer
Дата создания: 2025-10-07
"""

from typing import Dict, Any, List, Tuple
from pathlib import Path
import re


class ProjectDescriptionValidator:
    """
    Валидатор описания проектов Archon.

    Проверяет 4 обязательных поля:
    - description: что делает проект, цели, ключевые функции
    - tech_stack: язык, фреймворки, библиотеки, база данных
    - local_repo_path: полный путь на диске (например D:\\Automation\\Development\\projects\\patternshift)
    - git_repo: URL GitHub/GitLab репозитория
    """

    # Минимальная длина описания для считывания его полным
    MIN_DESCRIPTION_LENGTH = 50

    # Обязательные поля
    REQUIRED_FIELDS = [
        'description',
        'tech_stack',
        'local_repo_path',
        'git_repo'
    ]

    # Паттерны для валидации
    GIT_URL_PATTERN = re.compile(
        r'^https?://(github\.com|gitlab\.com)/[\w\-]+/[\w\-]+/?$'
    )

    PATH_PATTERN = re.compile(
        r'^[A-Za-z]:\\(?:[^<>:"/\\|?*]+\\)*[^<>:"/\\|?*]*$'
    )

    @staticmethod
    def validate_project_description(project_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Валидация полноты описания проекта.

        Args:
            project_data: Данные проекта из Archon (должны содержать поля из REQUIRED_FIELDS)

        Returns:
            Tuple[bool, List[str]]: (is_complete, list_of_missing_or_invalid_fields)

        Example:
            >>> project = {"description": "Test project", "tech_stack": "Python"}
            >>> is_valid, missing = ProjectDescriptionValidator.validate_project_description(project)
            >>> is_valid
            False
            >>> missing
            ['local_repo_path', 'git_repo']
        """
        missing_fields = []

        # Проверка наличия всех обязательных полей
        for field in ProjectDescriptionValidator.REQUIRED_FIELDS:
            if field not in project_data or not project_data[field]:
                missing_fields.append(field)
                continue

            # Специфическая валидация для каждого поля
            if field == 'description':
                if not ProjectDescriptionValidator._validate_description(project_data[field]):
                    missing_fields.append(f"{field} (слишком короткое: минимум {ProjectDescriptionValidator.MIN_DESCRIPTION_LENGTH} символов)")

            elif field == 'tech_stack':
                if not ProjectDescriptionValidator._validate_tech_stack(project_data[field]):
                    missing_fields.append(f"{field} (пустое или некорректное)")

            elif field == 'local_repo_path':
                if not ProjectDescriptionValidator._validate_local_path(project_data[field]):
                    missing_fields.append(f"{field} (некорректный путь)")

            elif field == 'git_repo':
                if not ProjectDescriptionValidator._validate_git_url(project_data[field]):
                    missing_fields.append(f"{field} (некорректный URL GitHub/GitLab)")

        is_complete = len(missing_fields) == 0
        return is_complete, missing_fields

    @staticmethod
    def _validate_description(description: str) -> bool:
        """
        Проверка описания проекта.

        Args:
            description: Текст описания

        Returns:
            bool: True если описание достаточно подробное
        """
        if not description or not isinstance(description, str):
            return False

        # Убираем лишние пробелы
        cleaned = description.strip()

        # Проверка минимальной длины
        return len(cleaned) >= ProjectDescriptionValidator.MIN_DESCRIPTION_LENGTH

    @staticmethod
    def _validate_tech_stack(tech_stack: str) -> bool:
        """
        Проверка технологического стека.

        Args:
            tech_stack: Описание технологий

        Returns:
            bool: True если tech_stack указан
        """
        if not tech_stack or not isinstance(tech_stack, str):
            return False

        # Проверка что не пустая строка
        return len(tech_stack.strip()) > 0

    @staticmethod
    def _validate_local_path(path: str) -> bool:
        """
        Проверка локального пути к репозиторию.

        Args:
            path: Путь на диске (например D:\\Automation\\Development\\projects\\patternshift)

        Returns:
            bool: True если путь корректный
        """
        if not path or not isinstance(path, str):
            return False

        # Проверка паттерна Windows пути
        if not ProjectDescriptionValidator.PATH_PATTERN.match(path):
            return False

        # Проверка существования пути (опционально, можно отключить если путь еще не создан)
        # path_obj = Path(path)
        # return path_obj.exists()

        return True

    @staticmethod
    def _validate_git_url(url: str) -> bool:
        """
        Проверка URL git репозитория.

        Args:
            url: URL GitHub/GitLab репозитория

        Returns:
            bool: True если URL корректный
        """
        if not url or not isinstance(url, str):
            return False

        # Проверка паттерна GitHub/GitLab URL
        return ProjectDescriptionValidator.GIT_URL_PATTERN.match(url) is not None

    @staticmethod
    def generate_interactive_prompts(missing_fields: List[str]) -> Dict[str, str]:
        """
        Генерация интерактивных промптов для заполнения недостающих полей.

        Args:
            missing_fields: Список недостающих полей

        Returns:
            Dict[str, str]: Словарь {field_name: prompt_text}

        Example:
            >>> missing = ['description', 'tech_stack']
            >>> prompts = ProjectDescriptionValidator.generate_interactive_prompts(missing)
            >>> 'description' in prompts
            True
        """
        prompts = {}

        for field in missing_fields:
            # Удаляем комментарии из имени поля если есть
            clean_field = field.split(' (')[0]

            if clean_field == 'description':
                prompts[clean_field] = (
                    "Описание проекта:\n"
                    "Что делает проект? Каковы его цели и ключевые функции?\n"
                    f"(минимум {ProjectDescriptionValidator.MIN_DESCRIPTION_LENGTH} символов)"
                )
            elif clean_field == 'tech_stack':
                prompts[clean_field] = (
                    "Технологический стек проекта:\n"
                    "Какой язык программирования, фреймворки, библиотеки используются?\n"
                    "Какая база данных? (например: Python, FastAPI, SQLAlchemy, PostgreSQL)"
                )
            elif clean_field == 'local_repo_path':
                prompts[clean_field] = (
                    "Локальный путь к репозиторию:\n"
                    "Полный путь на диске (например: D:\\Automation\\Development\\projects\\patternshift)\n"
                    "Используйте обратные слэши для Windows путей"
                )
            elif clean_field == 'git_repo':
                prompts[clean_field] = (
                    "URL Git репозитория:\n"
                    "GitHub или GitLab URL (например: https://github.com/username/repo)\n"
                    "Без .git в конце"
                )

        return prompts

    @staticmethod
    def format_validation_report(is_complete: bool, missing_fields: List[str]) -> str:
        """
        Форматирование отчета о валидации для вывода пользователю.

        Args:
            is_complete: Результат валидации
            missing_fields: Список недостающих полей

        Returns:
            str: Форматированный отчет
        """
        if is_complete:
            return "Описание проекта полное. Все обязательные поля заполнены."

        report_lines = [
            "Описание проекта НЕПОЛНОЕ!",
            "",
            "Недостающие или некорректные поля:",
        ]

        for i, field in enumerate(missing_fields, 1):
            report_lines.append(f"  {i}. {field}")

        report_lines.extend([
            "",
            "Необходимо заполнить недостающие поля для продолжения работы.",
            "Используйте интерактивный диалог создания описания."
        ])

        return "\n".join(report_lines)


# Пример использования
if __name__ == "__main__":
    # Тестовый проект с неполным описанием
    test_project_incomplete = {
        "title": "PatternShift",
        "description": "Short desc",  # Слишком короткое
        "tech_stack": "Python"
        # Отсутствуют local_repo_path и git_repo
    }

    is_valid, missing = ProjectDescriptionValidator.validate_project_description(test_project_incomplete)
    print(f"Проект валиден: {is_valid}")
    print(f"Недостающие поля: {missing}")
    print()
    print(ProjectDescriptionValidator.format_validation_report(is_valid, missing))
    print()

    # Генерация промптов для заполнения
    prompts = ProjectDescriptionValidator.generate_interactive_prompts(missing)
    for field, prompt in prompts.items():
        print(f"\n--- {field.upper()} ---")
        print(prompt)

    print("\n" + "="*60 + "\n")

    # Тестовый проект с полным описанием
    test_project_complete = {
        "title": "PatternShift",
        "description": "Трансформационная программа для психологов, использующая NLP и эриксоновский гипноз для создания персонализированных программ изменений",
        "tech_stack": "Python, FastAPI, Pydantic AI, PostgreSQL, Claude API",
        "local_repo_path": r"D:\Automation\Development\projects\patternshift",
        "git_repo": "https://github.com/username/patternshift"
    }

    is_valid, missing = ProjectDescriptionValidator.validate_project_description(test_project_complete)
    print(f"Проект валиден: {is_valid}")
    print(f"Недостающие поля: {missing}")
    print()
    print(ProjectDescriptionValidator.format_validation_report(is_valid, missing))
