# -*- coding: utf-8 -*-
"""
Спільні утиліти для Agent Factory.

Цей пакет містить інструменти та утиліти, які використовуються
всіма агентами фабрики.
"""

from .script_encoding_validator import (
    validate_script,
    validate_directory,
    fix_file_emojis,
    fix_directory_emojis,
    check_file_encoding,
    find_emojis_in_code,
    check_bom,
    remove_bom,
    EMOJI_REPLACEMENTS,
)

__all__ = [
    'validate_script',
    'validate_directory',
    'fix_file_emojis',
    'fix_directory_emojis',
    'check_file_encoding',
    'find_emojis_in_code',
    'check_bom',
    'remove_bom',
    'EMOJI_REPLACEMENTS',
]

__version__ = '1.0.0'
