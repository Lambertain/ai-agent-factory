# -*- coding: utf-8 -*-
"""
Модуль автоматического управления Git коммитами для агентов фабрики
Обеспечивает обязательные коммиты в конце задач и автоматический push
"""

import os
import sys
import subprocess
import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import asyncio

# Настройка логирования
logger = logging.getLogger(__name__)

@dataclass
class GitCommitConfig:
    """Конфигурация Git коммитов"""
    auto_commit_enabled: bool = True
    auto_push_enabled: bool = True
    commits_until_push: int = 5  # Автопуш каждые 5 коммитов
    backup_enabled: bool = True
    backup_dir: str = ""  # Автоопределяется
    commit_message_template: str = "feat: {task_description}\n\n🤖 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

    def __post_init__(self):
        if not self.backup_dir:
            # Определяем директорию для бэкапов
            project_root = Path.cwd()
            self.backup_dir = str(project_root / ".git_backups")

@dataclass
class GitCommitStats:
    """Статистика Git коммитов"""
    total_commits: int = 0
    commits_since_push: int = 0
    last_commit_hash: str = ""
    last_push_time: datetime = field(default_factory=datetime.now)
    last_backup_time: datetime = field(default_factory=datetime.now)
    failed_commits: List[str] = field(default_factory=list)
    failed_pushes: List[str] = field(default_factory=list)

class GitManager:
    """
    Менеджер автоматических Git операций для агентов фабрики

    Обеспечивает:
    - Автоматические коммиты в конце каждой задачи
    - Автоматический push каждые N коммитов
    - Создание бэкапов перед критическими операциями
    - Интеграцию с системой микрозадач
    - Отслеживание статистики коммитов
    """

    def __init__(self, config: Optional[GitCommitConfig] = None):
        self.config = config or GitCommitConfig()
        self.stats = GitCommitStats()
        self.stats_file = Path.cwd() / ".git_stats.json"
        self.load_stats()

        # Проверяем что мы в git репозитории
        self.repo_root = self._find_git_repo()
        if not self.repo_root:
            logger.warning("Git репозиторий не найден. Автокоммиты отключены.")
            self.config.auto_commit_enabled = False

    def _find_git_repo(self) -> Optional[Path]:
        """Найти корень git репозитория"""
        current = Path.cwd()

        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent

        return None

    def load_stats(self):
        """Загрузить статистику из файла"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.stats.total_commits = data.get('total_commits', 0)
                self.stats.commits_since_push = data.get('commits_since_push', 0)
                self.stats.last_commit_hash = data.get('last_commit_hash', '')

                # Парсим даты
                last_push_str = data.get('last_push_time')
                if last_push_str:
                    self.stats.last_push_time = datetime.fromisoformat(last_push_str)

                last_backup_str = data.get('last_backup_time')
                if last_backup_str:
                    self.stats.last_backup_time = datetime.fromisoformat(last_backup_str)

                self.stats.failed_commits = data.get('failed_commits', [])
                self.stats.failed_pushes = data.get('failed_pushes', [])

        except Exception as e:
            logger.warning(f"Не удалось загрузить статистику Git: {e}")

    def save_stats(self):
        """Сохранить статистику в файл"""
        try:
            data = {
                'total_commits': self.stats.total_commits,
                'commits_since_push': self.stats.commits_since_push,
                'last_commit_hash': self.stats.last_commit_hash,
                'last_push_time': self.stats.last_push_time.isoformat(),
                'last_backup_time': self.stats.last_backup_time.isoformat(),
                'failed_commits': self.stats.failed_commits,
                'failed_pushes': self.stats.failed_pushes
            }

            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Не удалось сохранить статистику Git: {e}")

    def _run_git_command(self, command: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str]:
        """Выполнить git команду"""
        try:
            if cwd is None:
                cwd = self.repo_root

            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )

            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()

        except subprocess.TimeoutExpired:
            return False, "Git команда превысила таймаут"
        except Exception as e:
            return False, str(e)

    def check_git_status(self) -> Tuple[bool, Dict[str, Any]]:
        """Проверить статус git репозитория"""
        if not self.repo_root:
            return False, {"error": "Git репозиторий не найден"}

        # Проверяем статус
        success, output = self._run_git_command(['git', 'status', '--porcelain'])
        if not success:
            return False, {"error": f"Не удалось получить статус: {output}"}

        # Парсим изменения
        changes = []
        if output:
            for line in output.split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:].strip()
                    changes.append({"status": status, "file": filename})

        # Проверяем текущую ветку
        success, branch = self._run_git_command(['git', 'branch', '--show-current'])
        if not success:
            branch = "unknown"

        # Проверяем удаленные изменения
        success, remote_status = self._run_git_command(['git', 'status', '-sb'])

        return True, {
            "branch": branch,
            "changes": changes,
            "has_changes": len(changes) > 0,
            "commits_since_push": self.stats.commits_since_push,
            "remote_status": remote_status if success else "unknown"
        }

    def create_backup(self, backup_name: str = "") -> Tuple[bool, str]:
        """Создать бэкап текущего состояния"""
        if not self.config.backup_enabled or not self.repo_root:
            return False, "Бэкапы отключены или нет Git репозитория"

        try:
            # Создаем директорию для бэкапов
            backup_dir = Path(self.config.backup_dir)
            backup_dir.mkdir(exist_ok=True)

            # Генерируем имя бэкапа
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"auto_backup_{timestamp}"

            backup_path = backup_dir / f"{backup_name}.zip"

            # Создаем архив с git репозиторием
            success, output = self._run_git_command([
                'git', 'archive',
                '--format=zip',
                f'--output={backup_path}',
                'HEAD'
            ])

            if success:
                self.stats.last_backup_time = datetime.now()
                self.save_stats()
                return True, f"Бэкап создан: {backup_path}"
            else:
                return False, f"Ошибка создания бэкапа: {output}"

        except Exception as e:
            return False, f"Ошибка создания бэкапа: {e}"

    def auto_commit_task_completion(self, task_description: str, files_changed: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Автоматический коммит при завершении задачи

        Args:
            task_description: Описание завершенной задачи
            files_changed: Список измененных файлов (если не указан - добавляем все)

        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        if not self.config.auto_commit_enabled or not self.repo_root:
            return False, "Автокоммиты отключены или нет Git репозитория"

        try:
            # Проверяем есть ли изменения
            status_ok, status_info = self.check_git_status()
            if not status_ok:
                return False, f"Не удалось проверить статус: {status_info.get('error', 'Неизвестная ошибка')}"

            if not status_info.get('has_changes', False):
                return False, "Нет изменений для коммита"

            # Создаем бэкап перед коммитом
            if self.config.backup_enabled:
                backup_success, backup_msg = self.create_backup(f"before_commit_{datetime.now().strftime('%H%M%S')}")
                if backup_success:
                    logger.info(backup_msg)

            # Добавляем файлы
            if files_changed:
                # Добавляем конкретные файлы
                for file_path in files_changed:
                    success, output = self._run_git_command(['git', 'add', file_path])
                    if not success:
                        logger.warning(f"Не удалось добавить файл {file_path}: {output}")
            else:
                # Добавляем все измененные файлы
                success, output = self._run_git_command(['git', 'add', '.'])
                if not success:
                    return False, f"Не удалось добавить файлы: {output}"

            # Создаем коммит
            commit_message = self.config.commit_message_template.format(
                task_description=task_description
            )

            success, output = self._run_git_command(['git', 'commit', '-m', commit_message])
            if not success:
                error_msg = f"Ошибка коммита: {output}"
                self.stats.failed_commits.append(f"{datetime.now().isoformat()}: {error_msg}")
                self.save_stats()
                return False, error_msg

            # Обновляем статистику
            self.stats.total_commits += 1
            self.stats.commits_since_push += 1

            # Получаем хэш коммита
            success, commit_hash = self._run_git_command(['git', 'rev-parse', 'HEAD'])
            if success:
                self.stats.last_commit_hash = commit_hash[:8]  # Короткий хэш

            self.save_stats()

            # Проверяем нужен ли автопуш
            commit_info = f"Коммит создан: {self.stats.last_commit_hash}"
            if self.stats.commits_since_push >= self.config.commits_until_push:
                push_success, push_msg = self.auto_push()
                if push_success:
                    commit_info += f"\nАвтопуш выполнен: {push_msg}"
                else:
                    commit_info += f"\nОшибка автопуша: {push_msg}"
            else:
                remaining = self.config.commits_until_push - self.stats.commits_since_push
                commit_info += f"\nДо автопуша осталось коммитов: {remaining}"

            return True, commit_info

        except Exception as e:
            error_msg = f"Ошибка автокоммита: {e}"
            self.stats.failed_commits.append(f"{datetime.now().isoformat()}: {error_msg}")
            self.save_stats()
            return False, error_msg

    def auto_push(self) -> Tuple[bool, str]:
        """
        Автоматический push в удаленный репозиторий

        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        if not self.config.auto_push_enabled or not self.repo_root:
            return False, "Автопуш отключен или нет Git репозитория"

        try:
            # Получаем текущую ветку
            success, branch = self._run_git_command(['git', 'branch', '--show-current'])
            if not success:
                return False, f"Не удалось определить текущую ветку: {branch}"

            # Пушим изменения
            success, output = self._run_git_command(['git', 'push', 'origin', branch])
            if not success:
                error_msg = f"Ошибка push: {output}"
                self.stats.failed_pushes.append(f"{datetime.now().isoformat()}: {error_msg}")
                self.save_stats()
                return False, error_msg

            # Обновляем статистику
            self.stats.commits_since_push = 0
            self.stats.last_push_time = datetime.now()
            self.save_stats()

            return True, f"Push выполнен в ветку {branch}"

        except Exception as e:
            error_msg = f"Ошибка автопуша: {e}"
            self.stats.failed_pushes.append(f"{datetime.now().isoformat()}: {error_msg}")
            self.save_stats()
            return False, error_msg

    def get_commit_stats(self) -> Dict[str, Any]:
        """Получить статистику коммитов"""
        return {
            "total_commits": self.stats.total_commits,
            "commits_since_push": self.stats.commits_since_push,
            "last_commit_hash": self.stats.last_commit_hash,
            "last_push_time": self.stats.last_push_time.isoformat(),
            "last_backup_time": self.stats.last_backup_time.isoformat(),
            "failed_commits_count": len(self.stats.failed_commits),
            "failed_pushes_count": len(self.stats.failed_pushes),
            "config": {
                "auto_commit_enabled": self.config.auto_commit_enabled,
                "auto_push_enabled": self.config.auto_push_enabled,
                "commits_until_push": self.config.commits_until_push,
                "backup_enabled": self.config.backup_enabled
            }
        }

    def format_commit_summary(self) -> str:
        """Форматированная сводка по коммитам"""
        stats = self.get_commit_stats()

        summary = []
        summary.append("GIT СТАТИСТИКА")
        summary.append("=" * 25)
        summary.append(f"Всего коммитов: {stats['total_commits']}")
        summary.append(f"Коммитов до push: {stats['commits_since_push']}/{self.config.commits_until_push}")

        if stats['last_commit_hash']:
            summary.append(f"Последний коммит: {stats['last_commit_hash']}")

        if stats['failed_commits_count'] > 0:
            summary.append(f"Неудачных коммитов: {stats['failed_commits_count']}")

        if stats['failed_pushes_count'] > 0:
            summary.append(f"Неудачных push: {stats['failed_pushes_count']}")

        summary.append("")
        summary.append("НАСТРОЙКИ:")
        summary.append(f"Автокоммиты: {'ON' if stats['config']['auto_commit_enabled'] else 'OFF'}")
        summary.append(f"Автопуш: {'ON' if stats['config']['auto_push_enabled'] else 'OFF'}")
        summary.append(f"Бэкапы: {'ON' if stats['config']['backup_enabled'] else 'OFF'}")

        return "\n".join(summary)


# Глобальный экземпляр менеджера
_global_git_manager = None

def get_git_manager() -> GitManager:
    """Получить глобальный экземпляр Git менеджера"""
    global _global_git_manager
    if _global_git_manager is None:
        _global_git_manager = GitManager()
    return _global_git_manager

# Функции-утилиты для интеграции в агенты

async def auto_commit_on_task_completion(task_description: str, files_changed: Optional[List[str]] = None) -> str:
    """
    Автоматический коммит при завершении задачи (async wrapper)

    Args:
        task_description: Описание завершенной задачи
        files_changed: Список измененных файлов

    Returns:
        Результат операции
    """
    git_manager = get_git_manager()
    success, message = git_manager.auto_commit_task_completion(task_description, files_changed)

    if success:
        return f"✓ Git коммит: {message}"
    else:
        return f"✗ Ошибка Git коммита: {message}"

def should_create_commit() -> bool:
    """Проверить нужно ли создавать коммит"""
    git_manager = get_git_manager()
    if not git_manager.config.auto_commit_enabled:
        return False

    status_ok, status_info = git_manager.check_git_status()
    return status_ok and status_info.get('has_changes', False)

def get_git_status_summary() -> str:
    """Получить краткую сводку статуса Git"""
    git_manager = get_git_manager()
    return git_manager.format_commit_summary()

# Экспорт для других модулей
__all__ = [
    'GitManager',
    'GitCommitConfig',
    'GitCommitStats',
    'get_git_manager',
    'auto_commit_on_task_completion',
    'should_create_commit',
    'get_git_status_summary'
]