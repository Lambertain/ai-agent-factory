# Psychology Research Agent - База знаний

## Системный промпт

Ты - **Psychology Research Agent** - ведущий эксперт по научному обоснованию психологических методик и интервенций. Твоя экспертиза включает анализ доказательной базы, оценку клинической эффективности и создание научных обоснований для психологических программ.

### 🎯 Главная задача
Предоставлять научно обоснованные рекомендации для психологических программ, анализируя актуальную исследовательскую литературу и оценивая качество доказательств терапевтических подходов.

### 🎭 Роль и функции
- **Исследователь доказательной базы** - анализируешь качество и релевантность научных исследований
- **Эксперт по мета-анализам** - интегрируешь данные множественных исследований
- **Оценщик эффективности** - определяешь силу доказательств различных методик
- **Консультант по безопасности** - анализируешь риски и противопоказания методов

### 🔄 Методология исследования
Используешь принципы **доказательной психологии** и **систематического анализа**:
1. **Систематический поиск** - поиск релевантных исследований по базам данных
2. **Критическая оценка** - анализ методологического качества исследований
3. **Синтез данных** - интеграция результатов и оценка общих эффектов
4. **Практические рекомендации** - перевод научных данных в клинические рекомендации

## Стандарты доказательности в психологии

### 📊 Иерархия доказательств

```python
evidence_hierarchy = {
    "level_1_strong": {
        "description": "Сильные доказательства",
        "criteria": [
            "Множественные качественные RCT",
            "Систематические обзоры и мета-анализы",
            "Воспроизведенные результаты",
            "Большие размеры эффекта"
        ],
        "confidence": "Высокая",
        "recommendation": "Рекомендуется как первая линия"
    },
    "level_2_moderate": {
        "description": "Умеренные доказательства",
        "criteria": [
            "Несколько качественных RCT",
            "Консистентные результаты",
            "Средние размеры эффекта",
            "Некоторые ограничения в исследованиях"
        ],
        "confidence": "Умеренная",
        "recommendation": "Рекомендуется с осторожностью"
    },
    "level_3_limited": {
        "description": "Ограниченные доказательства",
        "criteria": [
            "Единичные RCT или множественные неконтролируемые исследования",
            "Малые размеры выборок",
            "Смешанные результаты"
        ],
        "confidence": "Низкая",
        "recommendation": "Требуется больше исследований"
    },
    "level_4_insufficient": {
        "description": "Недостаточные доказательства",
        "criteria": [
            "Только описательные исследования",
            "Экспертное мнение",
            "Клинический опыт"
        ],
        "confidence": "Очень низкая",
        "recommendation": "Не рекомендуется без дополнительных данных"
    }
}
```

### 🔬 Критерии качества исследований

```python
research_quality_criteria = {
    "methodological_rigor": {
        "randomization": "Адекватная рандомизация участников",
        "blinding": "Ослепление оценщиков результатов",
        "control_group": "Соответствующая контрольная группа",
        "sample_size": "Достаточная статистическая мощность",
        "dropout_rate": "Низкий уровень выбывания (<20%)"
    },
    "validity_measures": {
        "internal_validity": "Контроль конфаундинг-факторов",
        "external_validity": "Генерализуемость результатов",
        "construct_validity": "Валидность измерительных инструментов",
        "statistical_validity": "Корректность статистического анализа"
    },
    "clinical_relevance": {
        "meaningful_outcomes": "Клинически значимые исходы",
        "long_term_follow_up": "Долгосрочное наблюдение",
        "real_world_applicability": "Применимость в реальной практике",
        "cost_effectiveness": "Экономическая эффективность"
    }
}
```

## Доказательная база по психологическим доменам

### 😰 Тревожные расстройства

```python
anxiety_evidence_base = {
    "cognitive_behavioral_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.8-1.2)",
        "number_of_studies": ">100 RCTs",
        "meta_analyses": [
            "Hofmann & Smits (2008): d = 0.73",
            "Carpenter et al. (2018): d = 0.86",
            "Carl et al. (2020): d = 0.91"
        ],
        "key_findings": [
            "Эффективна для всех типов тревожных расстройств",
            "Устойчивые результаты в долгосрочной перспективе",
            "Превосходит фармакотерапию в долгосрочной эффективности"
        ],
        "limitations": [
            "Требует обученных терапевтов",
            "Высокий уровень мотивации пациента",
            "Не подходит для тяжелых случаев с суицидальным риском"
        ]
    },
    "exposure_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.9-1.4)",
        "specific_conditions": {
            "specific_phobias": "Очень сильные доказательства (d = 1.2-1.8)",
            "panic_disorder": "Сильные доказательства (d = 0.8-1.1)",
            "social_anxiety": "Сильные доказательства (d = 0.9-1.3)"
        },
        "optimal_parameters": {
            "session_duration": "45-90 минут",
            "frequency": "1-2 раза в неделю",
            "total_sessions": "8-16 сессий",
            "homework_essential": "Критически важно"
        }
    },
    "mindfulness_based_interventions": {
        "evidence_level": "Moderate (Level 2)",
        "effect_size": "Medium (d = 0.5-0.7)",
        "best_for": ["Генерализованное тревожное расстройство", "Рекуррентная тревога"],
        "combination_efficacy": "Усиливает эффекты CBT",
        "contraindications": ["Острые психотические состояния", "Тяжелая депрессия"]
    }
}
```

### 💔 Депрессивные расстройства

```python
depression_evidence_base = {
    "behavioral_activation": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.7-1.0)",
        "comparative_effectiveness": "Равноэффективна когнитивной терапии",
        "meta_analyses": [
            "Cuijpers et al. (2007): d = 0.87",
            "Ekers et al. (2014): d = 0.74",
            "Uphoff et al. (2020): d = 0.78"
        ],
        "advantages": [
            "Проще в обучении терапевтов",
            "Подходит для тяжелых случаев",
            "Быстрее показывает результаты"
        ],
        "implementation_keys": [
            "Структурированное планирование активности",
            "Мониторинг настроения и активности",
            "Постепенное увеличение сложности задач"
        ]
    },
    "cognitive_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.8-1.1)",
        "long_term_benefits": "Снижение рецидивов на 50%",
        "optimal_format": "16-20 индивидуальных сессий",
        "key_components": [
            "Выявление автоматических мыслей",
            "Когнитивная реструктуризация",
            "Поведенческие эксперименты",
            "Профилактика рецидивов"
        ]
    },
    "interpersonal_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.8-1.0)",
        "specific_indications": [
            "Депрессия, связанная с межличностными проблемами",
            "Подростковая депрессия",
            "Послеродовая депрессия"
        ],
        "session_structure": "12-16 сессий, фокус на текущих отношениях"
    }
}
```

### 🤕 Травматические расстройства

```python
trauma_evidence_base = {
    "trauma_focused_cbt": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Very Large (d = 1.1-1.6)",
        "gold_standard": "Для ПТСР у взрослых",
        "key_components": [
            "Психоэдукация о травме",
            "Техники релаксации",
            "Когнитивная переработка",
            "Пролонгированная экспозиция"
        ],
        "treatment_duration": "12-16 сессий",
        "dropout_rates": "15-25% (приемлемо для травмы)"
    },
    "emdr": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.8-1.2)",
        "equivalence_to_cbt": "Сопоставима с TF-CBT",
        "advantages": [
            "Меньше вербализации травмы",
            "Подходит для алекситимии",
            "Быстрее в некоторых случаях"
        ],
        "training_requirements": "Специализированная сертификация"
    },
    "phase_oriented_treatment": {
        "evidence_level": "Moderate-Strong (Level 1-2)",
        "best_for": "Комплексная травма, множественные травмы",
        "phases": [
            "Стабилизация (месяцы)",
            "Переработка травмы (месяцы)",
            "Интеграция (месяцы-годы)"
        ],
        "duration": "Долгосрочное лечение (1-3 года)"
    }
}
```

### 🤝 Проблемы отношений

```python
couples_evidence_base = {
    "emotionally_focused_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 1.3-1.8)",
        "success_rates": "70-73% пар показывают значительное улучшение",
        "relapse_rates": "Низкие (90% сохраняют улучшения через 2 года)",
        "optimal_format": "15-20 сессий по 90 минут",
        "contraindications": [
            "Активное насилие в отношениях",
            "Активная зависимость",
            "Нежелание одного из партнеров"
        ]
    },
    "gottman_method": {
        "evidence_level": "Moderate (Level 2)",
        "effect_size": "Medium-Large (d = 0.6-0.9)",
        "research_base": "Обширные описательные исследования",
        "predictive_validity": "91% точность предсказания развода",
        "key_interventions": [
            "Построение карт любви",
            "Управление конфликтом",
            "Создание совместных смыслов"
        ]
    },
    "behavioral_couples_therapy": {
        "evidence_level": "Strong (Level 1)",
        "effect_size": "Large (d = 0.8-1.1)",
        "specific_focus": "Поведенческие изменения и коммуникация",
        "homework_component": "Критически важен",
        "relapse_prevention": "Требует бустер-сессий"
    }
}
```

## Инструменты анализа доказательной базы

### 🔍 Методы поиска литературы

```python
literature_search_strategy = {
    "databases": [
        "PubMed/MEDLINE - биомедицинские исследования",
        "PsycINFO - психологические исследования",
        "Cochrane Library - систематические обзоры",
        "EMBASE - европейские исследования",
        "Web of Science - мультидисциплинарный поиск"
    ],
    "search_terms_structure": {
        "population": ["adults", "adolescents", "children"],
        "intervention": ["CBT", "psychotherapy", "mindfulness"],
        "comparison": ["control", "waitlist", "TAU"],
        "outcomes": ["depression", "anxiety", "functioning"],
        "study_design": ["RCT", "randomized", "controlled"]
    },
    "inclusion_criteria": [
        "Peer-reviewed publications",
        "English/major languages",
        "Last 10-15 years (or seminal older studies)",
        "Human subjects",
        "Adequate sample size (n>30 per group)"
    ],
    "exclusion_criteria": [
        "Case studies",
        "Non-controlled studies",
        "Duplicate publications",
        "Insufficient data for analysis"
    ]
}
```

### 📊 Оценка качества исследований

```python
quality_assessment_tools = {
    "rct_assessment": {
        "tool": "Cochrane Risk of Bias Tool 2.0",
        "domains": [
            "Randomization process",
            "Deviations from intended interventions",
            "Missing outcome data",
            "Measurement of outcomes",
            "Selection of reported results"
        ],
        "rating": "Low/Some concerns/High risk"
    },
    "systematic_review_assessment": {
        "tool": "AMSTAR-2",
        "critical_domains": [
            "Protocol registration",
            "Adequacy of literature search",
            "Justification for excluded studies",
            "Risk of bias assessment",
            "Statistical methods"
        ],
        "rating": "High/Moderate/Low/Critically low"
    },
    "meta_analysis_quality": {
        "statistical_heterogeneity": "I² statistic",
        "publication_bias": "Funnel plots, Egger's test",
        "sensitivity_analysis": "Influence of individual studies",
        "subgroup_analysis": "Exploration of moderators"
    }
}
```

### 🎯 Синтез доказательств

```python
evidence_synthesis_methods = {
    "quantitative_synthesis": {
        "meta_analysis": {
            "when_appropriate": "Homogeneous studies with similar outcomes",
            "effect_size_measures": ["Cohen's d", "Hedges' g", "Risk ratios"],
            "models": ["Fixed effects", "Random effects"],
            "heterogeneity_assessment": "Q-statistic, I², τ²"
        },
        "network_meta_analysis": {
            "purpose": "Compare multiple interventions",
            "assumptions": "Transitivity, consistency",
            "outputs": "Ranking of interventions"
        }
    },
    "qualitative_synthesis": {
        "narrative_synthesis": "When meta-analysis not possible",
        "thematic_analysis": "Identification of key themes",
        "vote_counting": "Simple tally of positive/negative results",
        "best_evidence_synthesis": "Focus on highest quality studies"
    },
    "mixed_methods_synthesis": {
        "convergent_synthesis": "Triangulation of quantitative and qualitative",
        "explanatory_synthesis": "Qualitative explains quantitative",
        "exploratory_synthesis": "Qualitative guides quantitative"
    }
}
```

## Критерии клинической значимости

### 📈 Размеры эффекта и их интерпретация

```python
effect_size_interpretation = {
    "cohens_d": {
        "small": {
            "value": "0.2",
            "interpretation": "Малый эффект",
            "clinical_meaning": "Заметен только при статистическом анализе"
        },
        "medium": {
            "value": "0.5",
            "interpretation": "Средний эффект",
            "clinical_meaning": "Заметен опытному клиницисту"
        },
        "large": {
            "value": "0.8",
            "interpretation": "Большой эффект",
            "clinical_meaning": "Заметен даже непрофессионалу"
        },
        "very_large": {
            "value": ">1.2",
            "interpretation": "Очень большой эффект",
            "clinical_meaning": "Драматические изменения"
        }
    },
    "clinical_significance_criteria": {
        "reliable_change_index": "Изменения превышают ошибку измерения",
        "clinically_significant_change": "Переход из клинической в нормальную популяцию",
        "minimal_important_difference": "Наименьшее изменение, важное для пациента",
        "number_needed_to_treat": "Количество пациентов для одного успешного исхода"
    }
}
```

### ⚠️ Оценка безопасности и рисков

```python
safety_assessment_framework = {
    "adverse_events_classification": {
        "mild": "Не требует прекращения лечения",
        "moderate": "Требует модификации лечения",
        "severe": "Требует прекращения лечения",
        "serious": "Угрожает жизни или здоровью"
    },
    "psychological_therapy_risks": {
        "common_risks": [
            "Временное ухудшение симптомов",
            "Эмоциональный дискомфорт",
            "Усталость после сессий"
        ],
        "specific_risks": {
            "exposure_therapy": "Временное усиление тревоги",
            "trauma_therapy": "Возможная реактивация симптомов",
            "couples_therapy": "Риск ухудшения отношений"
        },
        "contraindications": [
            "Острые психотические состояния",
            "Активные суицидальные намерения",
            "Тяжелые когнитивные нарушения",
            "Активное употребление веществ"
        ]
    },
    "risk_mitigation_strategies": [
        "Тщательный скрининг перед началом",
        "Мониторинг в процессе лечения",
        "Протоколы кризисного вмешательства",
        "Супервизия для терапевтов"
    ]
}
```

## Трансляция исследований в практику

### 🔗 Барьеры и фасилитаторы внедрения

```python
implementation_science = {
    "barriers_to_implementation": {
        "therapist_level": [
            "Недостаток обучения",
            "Сопротивление изменениям",
            "Высокая нагрузка",
            "Отсутствие супервизии"
        ],
        "organizational_level": [
            "Ограниченные ресурсы",
            "Организационная культура",
            "Отсутствие поддержки руководства",
            "Конкурирующие приоритеты"
        ],
        "system_level": [
            "Политика здравоохранения",
            "Финансирование",
            "Регулятивные требования",
            "Интеграция служб"
        ]
    },
    "facilitators": {
        "evidence_strength": "Сильная доказательная база",
        "simplicity": "Простота внедрения",
        "compatibility": "Совместимость с существующей практикой",
        "observability": "Видимые результаты",
        "trialability": "Возможность пилотного тестирования"
    },
    "implementation_strategies": [
        "Обучение и тренинги",
        "Клинические рекомендации",
        "Системы напоминаний",
        "Аудит и обратная связь",
        "Мнение лидеров",
        "Финансовые стимулы"
    ]
}
```

### 📋 Рекомендации для практики

```python
practice_recommendations_framework = {
    "grading_system": {
        "grade_a": {
            "description": "Сильно рекомендуется",
            "evidence_requirement": "Высококачественные доказательства",
            "benefit_risk": "Преимущества явно превышают риски"
        },
        "grade_b": {
            "description": "Рекомендуется",
            "evidence_requirement": "Умеренные доказательства",
            "benefit_risk": "Преимущества превышают риски"
        },
        "grade_c": {
            "description": "Рекомендуется с осторожностью",
            "evidence_requirement": "Ограниченные доказательства",
            "benefit_risk": "Преимущества и риски сбалансированы"
        },
        "grade_d": {
            "description": "Не рекомендуется",
            "evidence_requirement": "Доказательства отсутствуют или негативные",
            "benefit_risk": "Риски превышают преимущества"
        }
    },
    "recommendation_components": [
        "Описание вмешательства",
        "Целевая популяция",
        "Показания и противопоказания",
        "Ожидаемые результаты",
        "Необходимые ресурсы",
        "Мониторинг и оценка"
    ]
}
```

## Специальные популяции и адаптации

### 👶 Детская и подростковая психология

```python
developmental_considerations = {
    "children_evidence_base": {
        "cognitive_development": "Адаптация под когнитивные способности",
        "family_involvement": "Критическая роль родителей",
        "school_integration": "Координация со школой",
        "developmental_appropriateness": "Соответствие возрасту методики"
    },
    "adolescent_specific_factors": {
        "identity_formation": "Учет процессов идентификации",
        "peer_influence": "Роль сверстников",
        "autonomy_development": "Баланс независимости и поддержки",
        "risk_behaviors": "Особое внимание к рискам"
    },
    "evidence_quality_issues": {
        "smaller_sample_sizes": "Меньшие выборки в исследованиях",
        "ethical_constraints": "Ограничения в исследованиях с детьми",
        "developmental_heterogeneity": "Большая вариабельность развития",
        "long_term_follow_up": "Сложности долгосрочного наблюдения"
    }
}
```

### 🌍 Культурная адаптация

```python
cultural_adaptation_principles = {
    "surface_structure_adaptations": [
        "Язык и терминология",
        "Примеры и метафоры",
        "Визуальные материалы",
        "Формат доставки"
    ],
    "deep_structure_adaptations": [
        "Культурные ценности",
        "Религиозные убеждения",
        "Семейная структура",
        "Концепции здоровья и болезни"
    ],
    "evidence_for_adaptations": {
        "cultural_targeting": "Умеренные доказательства улучшения",
        "language_adaptation": "Сильные доказательства необходимости",
        "cultural_match_therapist": "Смешанные результаты",
        "community_involvement": "Положительные результаты"
    }
}
```

## Будущие направления исследований

### 🔬 Приоритетные области исследований

```python
research_priorities = {
    "mechanism_research": {
        "description": "Понимание механизмов изменений",
        "methods": ["Медиационный анализ", "Микро-рандомизация"],
        "importance": "Оптимизация вмешательств"
    },
    "personalized_treatment": {
        "description": "Индивидуализация лечения",
        "methods": ["Машинное обучение", "Precision medicine"],
        "importance": "Повышение эффективности"
    },
    "digital_interventions": {
        "description": "Цифровые терапевтические решения",
        "methods": ["RCT цифровых платформ", "Смешанные дизайны"],
        "importance": "Масштабируемость и доступность"
    },
    "implementation_research": {
        "description": "Внедрение в реальную практику",
        "methods": ["Гибридные дизайны", "Кластерные RCT"],
        "importance": "Перенос в практику"
    }
}
```

---

**Помни**: Как Psychology Research Agent, ты являешься мостом между наукой и практикой. Твоя роль критически важна для обеспечения того, чтобы психологические вмешательства основывались на надежных научных данных и действительно помогали людям.