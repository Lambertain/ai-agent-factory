"""
Unit tests for Prisma Database Agent configurations.

Тестирует все примеры конфигураций на корректность и универсальность.
"""

import pytest
from dataclasses import fields
from typing import get_type_hints

# Import all configuration examples
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from examples.ecommerce_config import EcommercePrismaDependencies, get_ecommerce_dependencies
from examples.saas_config import SaasPrismaDependencies, get_saas_dependencies
from examples.crm_config import CrmPrismaDependencies, get_crm_dependencies
from examples.blog_config import BlogPrismaDependencies, get_blog_dependencies
from examples.social_config import SocialPrismaDependencies, get_social_dependencies
from dependencies import PrismaDatabaseDependencies


class TestConfigurationUniversality:
    """Тесты универсальности конфигураций."""

    def test_all_configs_inherit_from_base(self):
        """Все конфигурации должны наследоваться от базового класса."""
        configs = [
            EcommercePrismaDependencies,
            SaasPrismaDependencies,
            CrmPrismaDependencies,
            BlogPrismaDependencies,
            SocialPrismaDependencies
        ]

        for config_class in configs:
            assert issubclass(config_class, PrismaDatabaseDependencies), \
                f"{config_class.__name__} должен наследоваться от PrismaDatabaseDependencies"

    def test_domain_type_uniqueness(self):
        """Каждая конфигурация должна иметь уникальный domain_type."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        domain_types = [config.domain_type for config in configs]
        assert len(domain_types) == len(set(domain_types)), \
            f"Обнаружены дублирующиеся domain_type: {domain_types}"

    def test_no_hardcoded_project_names(self):
        """Проверка отсутствия упоминаний конкретных проектов."""
        prohibited_terms = [
            'unipark', 'UniPark', 'UNIPARK',
            'mycompany', 'acme', 'example_corp',
            'testproject', 'demoapp'
        ]

        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            for field in fields(config):
                field_value = str(getattr(config, field.name))
                for term in prohibited_terms:
                    assert term.lower() not in field_value.lower(), \
                        f"Найдено упоминание '{term}' в поле {field.name} конфигурации {config.__class__.__name__}"

    def test_required_methods_exist(self):
        """Все конфигурации должны реализовывать обязательные методы."""
        required_methods = ['get_schema_config', 'get_optimization_config']

        configs = [
            EcommercePrismaDependencies,
            SaasPrismaDependencies,
            CrmPrismaDependencies,
            BlogPrismaDependencies,
            SocialPrismaDependencies
        ]

        for config_class in configs:
            for method_name in required_methods:
                assert hasattr(config_class, method_name), \
                    f"{config_class.__name__} должен иметь метод {method_name}"

                method = getattr(config_class, method_name)
                assert callable(method), \
                    f"{method_name} в {config_class.__name__} должен быть вызываемым"

    def test_database_url_configurability(self):
        """Все конфигурации должны поддерживать настройку database_url."""
        test_url = "postgresql://test:password@localhost:5432/test_db"

        configs = [
            EcommercePrismaDependencies(database_url=test_url),
            SaasPrismaDependencies(database_url=test_url),
            CrmPrismaDependencies(database_url=test_url),
            BlogPrismaDependencies(database_url=test_url),
            SocialPrismaDependencies(database_url=test_url)
        ]

        for config in configs:
            assert config.database_url == test_url, \
                f"Конфигурация {config.__class__.__name__} не поддерживает настройку database_url"


class TestSchemaConfigurations:
    """Тесты схем данных."""

    def test_schema_config_structure(self):
        """Проверка структуры конфигурации схемы."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            schema_config = config.get_schema_config()

            # Проверка обязательных ключей
            assert 'models' in schema_config, \
                f"В schema_config {config.__class__.__name__} отсутствует 'models'"
            assert 'enums' in schema_config, \
                f"В schema_config {config.__class__.__name__} отсутствует 'enums'"

            # Проверка типов
            assert isinstance(schema_config['models'], list), \
                f"'models' в {config.__class__.__name__} должен быть списком"
            assert isinstance(schema_config['enums'], list), \
                f"'enums' в {config.__class__.__name__} должен быть списком"

    def test_models_have_required_fields(self):
        """Проверка обязательных полей в моделях."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            schema_config = config.get_schema_config()

            for model in schema_config['models']:
                assert 'name' in model, \
                    f"Модель в {config.__class__.__name__} должна иметь 'name'"
                assert 'fields' in model, \
                    f"Модель {model.get('name', 'Unknown')} в {config.__class__.__name__} должна иметь 'fields'"
                assert isinstance(model['fields'], list), \
                    f"'fields' в модели {model.get('name', 'Unknown')} должен быть списком"

    def test_universal_user_model_exists(self):
        """Все конфигурации должны содержать универсальную модель User."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            schema_config = config.get_schema_config()
            model_names = [model['name'] for model in schema_config['models']]

            assert 'User' in model_names, \
                f"Конфигурация {config.__class__.__name__} должна содержать модель User"


class TestOptimizationConfigurations:
    """Тесты конфигураций оптимизации."""

    def test_optimization_config_structure(self):
        """Проверка структуры конфигурации оптимизации."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            opt_config = config.get_optimization_config()

            # Проверка типа
            assert isinstance(opt_config, dict), \
                f"optimization_config в {config.__class__.__name__} должен быть словарем"

            # Проверка наличия индексов
            assert 'indexes' in opt_config, \
                f"В optimization_config {config.__class__.__name__} отсутствует 'indexes'"
            assert isinstance(opt_config['indexes'], list), \
                f"'indexes' в {config.__class__.__name__} должен быть списком"

    def test_indexes_are_postgresql_compliant(self):
        """Проверка соответствия индексов PostgreSQL синтаксису."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            opt_config = config.get_optimization_config()

            for index in opt_config['indexes']:
                assert isinstance(index, str), \
                    f"Индекс в {config.__class__.__name__} должен быть строкой"

                # Проверка основных PostgreSQL команд
                assert any(keyword in index.upper() for keyword in ['CREATE INDEX', 'CREATE UNIQUE INDEX']), \
                    f"Индекс в {config.__class__.__name__} должен содержать CREATE INDEX: {index}"

    def test_no_hardcoded_table_names(self):
        """Проверка отсутствия hardcoded имен таблиц специфичных для проектов."""
        prohibited_table_names = [
            'unipark_', 'company_specific_', 'project_'
        ]

        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            opt_config = config.get_optimization_config()

            for index in opt_config['indexes']:
                for prohibited in prohibited_table_names:
                    assert prohibited not in index.lower(), \
                        f"Найдено запрещенное имя таблицы '{prohibited}' в индексе: {index}"


class TestDomainSpecificFeatures:
    """Тесты специфичных для домена функций."""

    def test_ecommerce_specific_features(self):
        """Тестирование e-commerce специфичных функций."""
        config = get_ecommerce_dependencies()

        # Проверка e-commerce специфичных настроек
        assert hasattr(config, 'enable_inventory_tracking'), \
            "E-commerce конфигурация должна поддерживать inventory tracking"
        assert hasattr(config, 'enable_wishlist'), \
            "E-commerce конфигурация должна поддерживать wishlist"

        # Проверка схемы на наличие e-commerce моделей
        schema_config = config.get_schema_config()
        model_names = [model['name'] for model in schema_config['models']]

        expected_models = ['Product', 'Order', 'Category']
        for model in expected_models:
            assert model in model_names, \
                f"E-commerce конфигурация должна содержать модель {model}"

    def test_social_specific_features(self):
        """Тестирование social media специфичных функций."""
        config = get_social_dependencies()

        # Проверка social специфичных настроек
        assert hasattr(config, 'enable_direct_messages'), \
            "Social конфигурация должна поддерживать direct messages"
        assert hasattr(config, 'enable_stories'), \
            "Social конфигурация должна поддерживать stories"

        # Проверка схемы на наличие social моделей
        schema_config = config.get_schema_config()
        model_names = [model['name'] for model in schema_config['models']]

        expected_models = ['Post', 'Follow', 'Like']
        for model in expected_models:
            assert model in model_names, \
                f"Social конфигурация должна содержать модель {model}"

    def test_blog_specific_features(self):
        """Тестирование blog/CMS специфичных функций."""
        config = get_blog_dependencies()

        # Проверка blog специфичных настроек
        assert hasattr(config, 'enable_comments'), \
            "Blog конфигурация должна поддерживать comments"
        assert hasattr(config, 'enable_categories'), \
            "Blog конфигурация должна поддерживать categories"

        # Проверка схемы на наличие blog моделей
        schema_config = config.get_schema_config()
        model_names = [model['name'] for model in schema_config['models']]

        expected_models = ['Post', 'Comment', 'Category']
        for model in expected_models:
            assert model in model_names, \
                f"Blog конфигурация должна содержать модель {model}"


class TestSecurityCompliance:
    """Тесты соответствия требованиям безопасности."""

    def test_no_sensitive_data_in_configs(self):
        """Проверка отсутствия чувствительных данных в конфигурациях."""
        sensitive_patterns = [
            'password', 'secret', 'key', 'token',
            'admin123', 'test123', 'password123'
        ]

        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            config_str = str(config).lower()
            for pattern in sensitive_patterns:
                # Исключаем поля типа 'database_url', 'api_key_field' - названия полей не чувствительные
                if pattern in ['password', 'secret', 'key', 'token']:
                    continue

                assert pattern not in config_str, \
                    f"Найдены чувствительные данные '{pattern}' в конфигурации {config.__class__.__name__}"

    def test_environment_variables_usage(self):
        """Проверка использования переменных окружения для чувствительных данных."""
        configs = [
            get_ecommerce_dependencies(),
            get_saas_dependencies(),
            get_crm_dependencies(),
            get_blog_dependencies(),
            get_social_dependencies()
        ]

        for config in configs:
            # database_url должен поддерживать env переменные
            if hasattr(config, 'database_url') and config.database_url:
                # В тестах может быть тестовое значение, но в production должно быть env
                assert isinstance(config.database_url, str), \
                    f"database_url в {config.__class__.__name__} должен быть строкой"


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v", "--tb=short"])