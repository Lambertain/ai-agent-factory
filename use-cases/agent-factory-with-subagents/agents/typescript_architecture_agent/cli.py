"""Command line interface for TypeScript Architecture Agent."""

import asyncio
import click
from pathlib import Path
from typing import Optional
from .agent import run_typescript_analysis


@click.group()
def cli():
    """Универсальный TypeScript Architecture Agent для оптимизации проектов."""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--analysis-type', '-t',
              type=click.Choice(['full', 'types', 'performance', 'refactor']),
              default='full',
              help='Тип анализа для выполнения')
@click.option('--project-path', '-p',
              type=click.Path(),
              help='Путь к корню проекта')
@click.option('--output', '-o',
              type=click.Path(),
              help='Файл для сохранения результатов')
def analyze(file_path: str, analysis_type: str, project_path: Optional[str], output: Optional[str]):
    """Анализ TypeScript файла или проекта."""

    click.echo(f"🔍 Анализ TypeScript архитектуры: {file_path}")
    click.echo(f"📋 Тип анализа: {analysis_type}")

    # Подготовка контекста
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    context = f"Анализ файла: {file_path}\n\nСодержимое:\n{content}"

    # Запуск анализа
    try:
        result = asyncio.run(run_typescript_analysis(
            context=context,
            project_path=project_path or str(Path(file_path).parent),
            analysis_type=analysis_type
        ))

        click.echo("\n" + "="*50)
        click.echo("📊 РЕЗУЛЬТАТЫ АНАЛИЗА:")
        click.echo("="*50)
        click.echo(result)

        # Сохранение в файл если указано
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            click.echo(f"\n💾 Результаты сохранены в: {output}")

    except Exception as e:
        click.echo(f"❌ Ошибка анализа: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--fix-issues', is_flag=True,
              help='Автоматически исправить найденные проблемы')
@click.option('--report', '-r',
              type=click.Path(),
              help='Создать детальный отчет')
def audit(project_path: str, fix_issues: bool, report: Optional[str]):
    """Полный аудит TypeScript проекта."""

    click.echo(f"🏗️  Аудит TypeScript проекта: {project_path}")

    project = Path(project_path)

    # Поиск TypeScript файлов
    ts_files = list(project.rglob("*.ts")) + list(project.rglob("*.tsx"))

    if not ts_files:
        click.echo("❌ TypeScript файлы не найдены")
        return

    click.echo(f"📁 Найдено {len(ts_files)} TypeScript файлов")

    results = []

    with click.progressbar(ts_files, label='Анализ файлов') as files:
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                context = f"Аудит проекта - файл: {file_path}\n\nСодержимое:\n{content}"

                result = asyncio.run(run_typescript_analysis(
                    context=context,
                    project_path=project_path,
                    analysis_type='full'
                ))

                results.append({
                    'file': str(file_path),
                    'result': result
                })

            except Exception as e:
                click.echo(f"\n⚠️  Ошибка в файле {file_path}: {e}")

    # Создание отчета
    if report:
        with open(report, 'w', encoding='utf-8') as f:
            f.write("# TypeScript Architecture Audit Report\n\n")
            f.write(f"Проект: {project_path}\n")
            f.write(f"Проанализировано файлов: {len(results)}\n\n")

            for i, result in enumerate(results, 1):
                f.write(f"## {i}. {result['file']}\n\n")
                f.write(result['result'])
                f.write("\n\n---\n\n")

        click.echo(f"\n📄 Отчет сохранен: {report}")

    click.echo("\n✅ Аудит завершен")


@cli.command()
@click.argument('code', type=str)
@click.option('--strategy', '-s',
              type=click.Choice(['optimize', 'simplify', 'strengthen']),
              default='optimize',
              help='Стратегия рефакторинга')
def refactor(code: str, strategy: str):
    """Рефакторинг TypeScript кода."""

    click.echo(f"🔧 Рефакторинг TypeScript кода")
    click.echo(f"📋 Стратегия: {strategy}")

    context = f"Рефакторинг кода со стратегией '{strategy}':\n\n{code}"

    try:
        result = asyncio.run(run_typescript_analysis(
            context=context,
            analysis_type='refactor'
        ))

        click.echo("\n" + "="*50)
        click.echo("🔧 РЕЗУЛЬТАТЫ РЕФАКТОРИНГА:")
        click.echo("="*50)
        click.echo(result)

    except Exception as e:
        click.echo(f"❌ Ошибка рефакторинга: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--project-path', '-p',
              type=click.Path(),
              default='.',
              help='Путь к проекту')
def optimize_config(project_path: str):
    """Оптимизация конфигурации TypeScript."""

    click.echo(f"⚙️  Оптимизация tsconfig.json для проекта: {project_path}")

    context = f"Оптимизация TypeScript конфигурации для проекта в {project_path}"

    try:
        result = asyncio.run(run_typescript_analysis(
            context=context,
            project_path=project_path,
            analysis_type='performance'
        ))

        click.echo("\n" + "="*50)
        click.echo("⚙️  ОПТИМИЗИРОВАННАЯ КОНФИГУРАЦИЯ:")
        click.echo("="*50)
        click.echo(result)

    except Exception as e:
        click.echo(f"❌ Ошибка оптимизации: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()