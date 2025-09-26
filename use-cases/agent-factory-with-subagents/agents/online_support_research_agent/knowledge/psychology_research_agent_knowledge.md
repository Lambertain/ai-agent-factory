# Psychology Research Agent Knowledge Base

## Системный промпт

Вы - эксперт по психологическим исследованиям и научной валидации психологического контента. Ваша специализация включает:

**Исследовательская методология:**
- Дизайн исследований (экспериментальные, корреляционные, лонгитюдные)
- Статистический анализ и интерпретация данных
- Валидация психометрических инструментов
- Мета-анализ и систематические обзоры

**Научная валидация:**
- Проверка соответствия научным стандартам
- Анализ методологических ошибок
- Оценка качества доказательной базы
- Соответствие принципам evidence-based practice

**Этические аспекты исследований:**
- Информированное согласие и конфиденциальность
- Минимизация рисков для участников
- Культурная чувствительность в исследованиях
- Соблюдение международных стандартов

**Области экспертизы:**
- Клиническая психология и психотерапия
- Когнитивная и экспериментальная психология
- Социальная и организационная психология
- Психология развития и образовательная психология
- Психометрика и психодиагностика

Вы обеспечиваете научную строгость, методологическую корректность и этическое соответствие психологических программ и исследований.

## Ключевые паттерны исследовательской валидации

### 1. Анализ дизайна исследования

```python
# Пример анализа методологии
research_design_criteria = {
    "experimental_design": {
        "randomization": "proper/inadequate/absent",
        "control_groups": "appropriate/inadequate/missing",
        "blinding": "double/single/none",
        "power_analysis": "adequate/inadequate/missing"
    },
    "sampling": {
        "population_definition": "clear/unclear",
        "sample_size": "adequate/inadequate",
        "representativeness": "high/medium/low",
        "inclusion_exclusion": "appropriate/problematic"
    },
    "measurement": {
        "validated_instruments": "yes/partially/no",
        "reliability_reported": "yes/no",
        "validity_evidence": "strong/moderate/weak"
    }
}
```

### 2. Статистическая валидация

```python
# Критерии статистического анализа
statistical_validity = {
    "effect_size": {
        "reported": True/False,
        "magnitude": "large/medium/small/trivial",
        "confidence_intervals": True/False
    },
    "multiple_comparisons": {
        "correction_applied": "bonferroni/fdr/none",
        "family_wise_error": "controlled/uncontrolled"
    },
    "assumptions": {
        "normality_checked": True/False,
        "homogeneity_verified": True/False,
        "independence_assumed": True/False
    },
    "power_analysis": {
        "prospective": True/False,
        "retrospective": True/False,
        "adequate_power": True/False
    }
}
```

### 3. Психометрическая оценка

```python
# Валидация психометрических свойств
psychometric_validation = {
    "reliability": {
        "internal_consistency": "cronbach_alpha >= 0.70",
        "test_retest": "r >= 0.70",
        "inter_rater": "ICC >= 0.75"
    },
    "validity": {
        "content_validity": "expert_panel_rating >= 0.80",
        "construct_validity": "factor_structure_confirmed",
        "criterion_validity": "concurrent/predictive_r >= 0.30",
        "discriminant_validity": "HTMT < 0.85"
    },
    "item_analysis": {
        "item_difficulty": "0.20 - 0.80",
        "item_discrimination": ">= 0.30",
        "distractor_analysis": "functional/non_functional"
    }
}
```

## Стандарты научной валидации

### Иерархия доказательств в психологии

1. **Мета-анализы и систематические обзоры**
   - Кокрановские обзоры
   - Мета-анализы RCT
   - Систематические обзоры высокого качества

2. **Рандомизированные контролируемые исследования (RCT)**
   - Двойное слепое плацебо-контролируемое
   - Одинарное слепое контролируемое
   - Открытое контролируемое

3. **Нерандомизированные контролируемые исследования**
   - Квази-экспериментальные
   - Когортные проспективные
   - Case-control исследования

4. **Описательные исследования**
   - Поперечные исследования
   - Серии случаев
   - Отдельные случаи

### Критерии оценки качества исследований

```markdown
## Чек-лист качества исследования (CONSORT/STROBE адаптация)

### Дизайн и методология:
- [ ] Четко определенные цели и гипотезы
- [ ] Обоснованный выбор дизайна исследования
- [ ] Адекватная процедура рандомизации (для RCT)
- [ ] Ослепление участников и исследователей
- [ ] Предварительный расчет размера выборки

### Участники:
- [ ] Четкие критерии включения/исключения
- [ ] Репрезентативная выборка
- [ ] Адекватный размер выборки
- [ ] Минимальный отсев участников (<20%)
- [ ] Анализ характеристик выбывших

### Вмешательства:
- [ ] Детальное описание вмешательства
- [ ] Стандартизованные протоколы
- [ ] Контроль верности вмешательству
- [ ] Адекватная контрольная группа

### Измерения:
- [ ] Валидированные инструменты
- [ ] Множественные источники данных
- [ ] Ослепленная оценка исходов
- [ ] Предварительно определенные первичные исходы

### Статистический анализ:
- [ ] Предварительно определенный план анализа
- [ ] Intention-to-treat анализ
- [ ] Множественная импутация пропущенных данных
- [ ] Поправка на множественные сравнения
- [ ] Отчет о размерах эффекта и доверительных интервалах
```

## Инструменты и методы исследовательской валидации

### 1. Поиск и анализ литературы

```python
# Стратегия систематического поиска
literature_search = {
    "databases": [
        "PubMed/MEDLINE",
        "PsycINFO",
        "Cochrane Library",
        "Web of Science",
        "Embase",
        "CINAHL"
    ],
    "search_strategy": {
        "keywords": ["psychology", "validation", "methodology"],
        "mesh_terms": True,
        "boolean_operators": "AND/OR/NOT",
        "date_limits": "last_10_years",
        "language": "english",
        "study_types": ["RCT", "meta-analysis", "systematic_review"]
    },
    "screening_criteria": {
        "title_abstract": "independent_dual_review",
        "full_text": "independent_dual_review",
        "disagreement_resolution": "third_reviewer"
    }
}
```

### 2. Критическая оценка исследований

```python
# Инструменты оценки качества
quality_assessment_tools = {
    "RCT": {
        "cochrane_rob": "Risk of Bias tool",
        "jadad_scale": "0-5 points",
        "pedro_scale": "physiotherapy evidence"
    },
    "observational": {
        "newcastle_ottawa": "cohort/case-control",
        "strobe_checklist": "reporting quality",
        "casp_tools": "critical appraisal"
    },
    "systematic_reviews": {
        "amstar": "methodological quality",
        "robis": "risk of bias",
        "grade": "evidence certainty"
    },
    "diagnostic": {
        "quadas": "diagnostic accuracy",
        "stard": "reporting standards"
    }
}
```

### 3. Мета-анализ и количественный синтез

```python
# Мета-аналитические методы
meta_analysis_methods = {
    "effect_sizes": {
        "continuous": "cohen_d, hedges_g, glass_delta",
        "binary": "odds_ratio, risk_ratio, risk_difference",
        "correlation": "fisher_z_transform"
    },
    "heterogeneity": {
        "q_statistic": "chi_square_test",
        "i_squared": "percentage_variance",
        "tau_squared": "between_study_variance"
    },
    "models": {
        "fixed_effects": "common_effect_assumption",
        "random_effects": "between_study_variation",
        "mixed_effects": "moderator_analysis"
    },
    "publication_bias": {
        "funnel_plot": "visual_inspection",
        "egger_test": "statistical_test",
        "trim_fill": "adjustment_method"
    }
}
```

## Специфичные для психологии критерии валидации

### 1. Клиническая психология

```python
clinical_validation_criteria = {
    "therapeutic_interventions": {
        "evidence_levels": {
            "well_established": ">= 2 RCT by independent teams",
            "probably_efficacious": "1 RCT or >= 2 controlled studies",
            "possibly_efficacious": "1 controlled study",
            "experimental": "case studies only"
        },
        "outcome_measures": {
            "primary": "symptom_severity_scales",
            "secondary": "functional_outcomes, QoL",
            "process": "therapeutic_alliance, engagement"
        }
    },
    "diagnostic_tools": {
        "sensitivity": ">= 0.80",
        "specificity": ">= 0.80",
        "ppv": ">= 0.50",
        "npv": ">= 0.90",
        "diagnostic_odds_ratio": ">= 10"
    }
}
```

### 2. Когнитивная психология

```python
cognitive_validation_criteria = {
    "experimental_paradigms": {
        "reaction_time": {
            "outlier_handling": "3SD or IQR method",
            "practice_effects": "sufficient_trials",
            "ceiling_floor": "< 15% participants"
        },
        "accuracy_measures": {
            "chance_level": "significantly_above",
            "learning_curves": "asymptotic_performance",
            "transfer_effects": "near/far_transfer"
        }
    },
    "cognitive_models": {
        "model_fitting": {
            "goodness_of_fit": "R² >= 0.70",
            "parameter_recovery": "simulation_based",
            "model_comparison": "AIC, BIC, cross_validation"
        }
    }
}
```

### 3. Социальная психология

```python
social_validation_criteria = {
    "experimental_design": {
        "ecological_validity": "real_world_relevance",
        "demand_characteristics": "minimized",
        "social_desirability": "controlled_for",
        "cultural_factors": "considered"
    },
    "replication": {
        "direct_replication": "same_procedures",
        "conceptual_replication": "different_operationalization",
        "cross_cultural": "multiple_populations",
        "meta_analytic": "effect_size_consistency"
    }
}
```

## Этические стандарты исследований

### Принципы исследовательской этики

1. **Автономия и информированное согласие**
   - Добровольность участия
   - Право на отказ без последствий
   - Полная информация о процедурах
   - Понимание рисков и преимуществ

2. **Благодеяние и непричинение вреда**
   - Минимизация рисков
   - Максимизация пользы
   - Соотношение риск/польза
   - Защита уязвимых групп

3. **Справедливость**
   - Справедливое распределение участников
   - Доступность результатов
   - Отсутствие дискриминации
   - Учет культурных различий

4. **Конфиденциальность и приватность**
   - Защита персональных данных
   - Анонимизация результатов
   - Безопасное хранение данных
   - Ограниченный доступ

### Специальные этические соображения

```python
ethical_considerations = {
    "vulnerable_populations": {
        "children": "parental_consent + child_assent",
        "cognitive_impairment": "capacity_assessment",
        "psychiatric_patients": "independent_advocate",
        "prisoners": "additional_safeguards"
    },
    "deception_studies": {
        "justification": "scientific_necessity",
        "minimization": "least_deceptive_method",
        "debriefing": "immediate_and_complete",
        "withdrawal": "post_debriefing_option"
    },
    "online_research": {
        "informed_consent": "digital_documentation",
        "data_security": "encryption_required",
        "anonymity": "ip_address_handling",
        "jurisdiction": "cross_border_compliance"
    }
}
```

## Отчетность и документация

### Стандарты отчетности

1. **CONSORT** - рандомизированные исследования
2. **STROBE** - наблюдательные исследования
3. **PRISMA** - систематические обзоры
4. **STARD** - диагностические исследования
5. **COREQ** - качественные исследования

### Требования к документации

```python
documentation_requirements = {
    "protocol": {
        "pre_registration": "clinical_trials_registry",
        "statistical_plan": "detailed_analysis_plan",
        "primary_outcomes": "clearly_defined",
        "sample_size": "power_calculation_included"
    },
    "data_management": {
        "data_dictionary": "variable_definitions",
        "quality_control": "range_checks_outliers",
        "audit_trail": "changes_documented",
        "backup_procedures": "regular_secure_backups"
    },
    "reporting": {
        "flow_diagram": "participant_flow",
        "baseline_table": "group_characteristics",
        "results_table": "effect_sizes_CI",
        "discussion": "limitations_addressed"
    }
}
```

## Интеграция с проектами исследований

### Поддержка исследовательских проектов

```python
research_project_support = {
    "planning_phase": {
        "literature_review": "systematic_search_strategy",
        "hypothesis_development": "theory_based_predictions",
        "design_optimization": "power_analysis_simulation",
        "ethical_approval": "irb_submission_support"
    },
    "implementation": {
        "protocol_adherence": "quality_monitoring",
        "data_collection": "standardized_procedures",
        "interim_analysis": "stopping_rules_defined",
        "adverse_events": "reporting_procedures"
    },
    "analysis_reporting": {
        "statistical_analysis": "appropriate_methods",
        "interpretation": "clinical_significance",
        "dissemination": "publication_strategy",
        "knowledge_translation": "practice_implications"
    }
}
```

### Междисциплинарное сотрудничество

```python
collaboration_framework = {
    "statistical_consultation": {
        "study_design": "biostatistician_input",
        "analysis_plan": "statistical_review",
        "interpretation": "clinical_statistical_dialogue"
    },
    "methodological_expertise": {
        "measurement": "psychometrician_consultation",
        "design": "epidemiologist_input",
        "qualitative": "qualitative_researcher_collaboration"
    },
    "domain_expertise": {
        "clinical": "practicing_clinicians",
        "educational": "education_researchers",
        "organizational": "IO_psychologists"
    }
}
```

## Технологические инструменты исследований

### Программное обеспечение для анализа

```python
research_software = {
    "statistical_packages": {
        "r": "comprehensive_statistical_environment",
        "spss": "user_friendly_interface",
        "stata": "econometric_focus",
        "sas": "enterprise_solutions",
        "jamovi": "open_source_spss_alternative"
    },
    "specialized_tools": {
        "mplus": "structural_equation_modeling",
        "comprehensive_meta_analysis": "meta_analysis",
        "revman": "cochrane_reviews",
        "maxqda": "qualitative_analysis",
        "eprime": "experimental_psychology"
    },
    "online_platforms": {
        "qualtrics": "survey_research",
        "redcap": "clinical_data_capture",
        "prolific": "participant_recruitment",
        "osf": "open_science_framework"
    }
}
```

### Автоматизация и воспроизводимость

```python
reproducible_research = {
    "version_control": {
        "git": "code_versioning",
        "github": "collaboration_platform",
        "protocols_io": "method_sharing"
    },
    "computational_notebooks": {
        "jupyter": "python_r_integration",
        "r_markdown": "dynamic_documents",
        "observable": "interactive_analysis"
    },
    "containerization": {
        "docker": "environment_reproducibility",
        "binder": "executable_publications",
        "code_ocean": "computational_reproducibility"
    }
}
```

## Показатели эффективности исследований

### Научные метрики

```python
research_metrics = {
    "publication_metrics": {
        "impact_factor": "journal_citation_rate",
        "h_index": "researcher_productivity",
        "altmetrics": "social_media_attention",
        "open_access": "accessibility_score"
    },
    "research_quality": {
        "replication_rate": "reproducibility_measure",
        "citation_accuracy": "reference_verification",
        "data_sharing": "transparency_indicator",
        "preregistration": "bias_prevention"
    },
    "societal_impact": {
        "policy_citations": "government_documents",
        "media_coverage": "public_engagement",
        "clinical_guidelines": "practice_integration",
        "patent_citations": "innovation_transfer"
    }
}
```

### Непрерывное улучшение

```python
quality_improvement = {
    "peer_review": {
        "pre_submission": "colleague_feedback",
        "journal_review": "expert_evaluation",
        "post_publication": "community_discussion"
    },
    "training_development": {
        "methodology_courses": "skill_enhancement",
        "statistical_literacy": "analysis_competency",
        "ethics_training": "responsible_conduct",
        "open_science": "transparency_practices"
    },
    "community_engagement": {
        "professional_societies": "knowledge_sharing",
        "conferences": "networking_learning",
        "mentorship": "next_generation_training",
        "public_outreach": "science_communication"
    }
}
```

Эта база знаний обеспечивает Psychology Research Agent всем необходимым для выполнения высококачественной научной валидации и поддержки исследовательских проектов в области психологии.