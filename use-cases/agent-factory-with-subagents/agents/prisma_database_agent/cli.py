"""Command line interface для Prisma Database Agent."""

import asyncio
import click
from pathlib import Path
from typing import Optional
from .agent import run_prisma_analysis


@click.group()
def cli():
    """Prisma Database Agent для универсальной работы с базами данных."""
    pass


@cli.command()
@click.argument('schema_path', type=click.Path(exists=True))
@click.option('--analysis-type', '-t',
              type=click.Choice(['full', 'schema', 'queries', 'migrations', 'performance']),
              default='full',
              help='Тип анализа для выполнения')
@click.option('--project-path', '-p',
              type=click.Path(),
              help='Путь к корню проекта')
@click.option('--output', '-o',
              type=click.Path(),
              help='Файл для сохранения результатов')
def analyze_schema(schema_path: str, analysis_type: str, project_path: Optional[str], output: Optional[str]):
    """Анализ Prisma схемы."""

    click.echo(f"🗄️ Анализ Prisma схемы: {schema_path}")
    click.echo(f"📋 Тип анализа: {analysis_type}")

    # Чтение схемы
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    context = f"Анализ Prisma схемы: {schema_path}\n\nСодержимое:\n{schema_content}"

    # Запуск анализа
    try:
        result = asyncio.run(run_prisma_analysis(
            context=context,
            project_path=project_path or str(Path(schema_path).parent),
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
@click.argument('query', type=str)
@click.option('--query-type', '-t',
              type=click.Choice(['select', 'create', 'update', 'delete']),
              default='select',
              help='Тип Prisma запроса')
@click.option('--output', '-o',
              type=click.Path(),
              help='Файл для сохранения оптимизированного запроса')
def optimize_query(query: str, query_type: str, output: Optional[str]):
    """Оптимизация Prisma запроса."""

    click.echo(f"⚡ Оптимизация {query_type} запроса")
    click.echo(f"📝 Исходный запрос: {query[:100]}...")

    context = f"Оптимизация Prisma {query_type} запроса:\n\n{query}"

    try:
        result = asyncio.run(run_prisma_analysis(
            context=context,
            analysis_type="queries"
        ))

        click.echo("\n" + "="*50)
        click.echo("⚡ ОПТИМИЗИРОВАННЫЙ ЗАПРОС:")
        click.echo("="*50)
        click.echo(result)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            click.echo(f"\n💾 Результаты сохранены в: {output}")

    except Exception as e:
        click.echo(f"❌ Ошибка оптимизации: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('changes', type=str)
@click.option('--production', is_flag=True,
              help='Создать план для production окружения')
@click.option('--backup', is_flag=True,
              help='Включить создание backup в план')
@click.option('--output', '-o',
              type=click.Path(),
              help='Файл для сохранения плана миграции')
def create_migration(changes: str, production: bool, backup: bool, output: Optional[str]):
    """Создание плана миграции."""

    click.echo(f"📋 Создание плана миграции")
    click.echo(f"🔄 Изменения: {changes}")
    click.echo(f"🏭 Production режим: {'Да' if production else 'Нет'}")

    context = f"Создание плана миграции для изменений:\n\n{changes}"
    if production:
        context += "\n\nТребования: production-ready миграция с полными backup'ами"
    if backup:
        context += "\n\nОбязательно: создание backup'ов данных"

    try:
        result = asyncio.run(run_prisma_analysis(
            context=context,
            analysis_type="migrations"
        ))

        click.echo("\n" + "="*50)
        click.echo("📋 ПЛАН МИГРАЦИИ:")
        click.echo("="*50)
        click.echo(result)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            click.echo(f"\n💾 План сохранен в: {output}")

    except Exception as e:
        click.echo(f"❌ Ошибка создания плана: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('query_log', type=click.Path(exists=True))
@click.option('--threshold', '-t',
              type=float,
              default=1000.0,
              help='Порог медленных запросов в миллисекундах')
@click.option('--limit', '-l',
              type=int,
              default=10,
              help='Количество запросов для анализа')
@click.option('--output', '-o',
              type=click.Path(),
              help='Файл для сохранения анализа')
def analyze_slow_queries(query_log: str, threshold: float, limit: int, output: Optional[str]):
    """Анализ медленных запросов из лога."""

    click.echo(f"🐌 Анализ медленных запросов из: {query_log}")
    click.echo(f"⏱️ Порог времени: {threshold}ms")
    click.echo(f"📊 Лимит запросов: {limit}")

    # Чтение лога
    with open(query_log, 'r', encoding='utf-8') as f:
        log_content = f.read()

    context = f"Анализ медленных запросов (порог: {threshold}ms):\n\n{log_content[:5000]}..."

    try:
        result = asyncio.run(run_prisma_analysis(
            context=context,
            analysis_type="performance"
        ))

        click.echo("\n" + "="*50)
        click.echo("🐌 АНАЛИЗ МЕДЛЕННЫХ ЗАПРОСОВ:")
        click.echo("="*50)
        click.echo(result)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            click.echo(f"\n💾 Анализ сохранен в: {output}")

    except Exception as e:
        click.echo(f"❌ Ошибка анализа: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--check-performance', is_flag=True,
              help='Включить анализ производительности')
@click.option('--suggest-indexes', is_flag=True,
              help='Предложить оптимизацию индексов')
@click.option('--report', '-r',
              type=click.Path(),
              help='Создать детальный отчет')
def audit_database(project_path: str, check_performance: bool, suggest_indexes: bool, report: Optional[str]):
    """Полный аудит базы данных проекта."""

    click.echo(f"🔍 Полный аудит базы данных: {project_path}")

    project = Path(project_path)
    schema_file = project / "prisma" / "schema.prisma"

    if not schema_file.exists():
        click.echo("❌ Файл schema.prisma не найден")
        return

    # Чтение схемы
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    context = f"Полный аудит базы данных проекта:\n\nПуть: {project_path}\n\nПrisma схема:\n{schema_content}"

    if check_performance:
        context += "\n\nТребования: детальный анализ производительности"
    if suggest_indexes:
        context += "\n\nТребования: рекомендации по оптимизации индексов"

    try:
        result = asyncio.run(run_prisma_analysis(
            context=context,
            project_path=project_path,
            analysis_type="full"
        ))

        click.echo("\n" + "="*60)
        click.echo("🔍 РЕЗУЛЬТАТЫ АУДИТА:")
        click.echo("="*60)
        click.echo(result)

        # Создание отчета
        if report:
            with open(report, 'w', encoding='utf-8') as f:
                f.write("# Database Audit Report\n\n")
                f.write(f"Проект: {project_path}\n")
                f.write(f"Дата аудита: {click.DateTime().now()}\n\n")
                f.write("## Результаты анализа\n\n")
                f.write(result)

            click.echo(f"\n📄 Отчет сохранен: {report}")

        click.echo("\n✅ Аудит завершен")

    except Exception as e:
        click.echo(f"❌ Ошибка аудита: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()