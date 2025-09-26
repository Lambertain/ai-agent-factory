/**
 * Domain Settings - Configuration for different psychological domains
 * Universal domain configuration system for psychological content creation
 */

const domainSettings = {
    // === Core Psychology Domains ===
    'general-psychology': {
        name: 'General Psychology',
        description: 'Broad psychological principles and applications',
        requirements: [
            'evidence-based-approach',
            'ethical-considerations',
            'cultural-sensitivity',
            'individual-differences'
        ],
        validation: [
            'scientific-accuracy',
            'practical-applicability',
            'ethical-compliance',
            'accessibility'
        ],
        approaches: [
            'cognitive-behavioral',
            'humanistic',
            'integrative',
            'evidence-based'
        ],
        integrationStrategy: 'holistic',
        qualityThreshold: 0.80,
        preferredAgents: ['research', 'domain-expert', 'nlp-generator', 'quality-guardian'],
        specializations: {
            'cognitive': ['cognitive-psychology', 'thinking-patterns', 'mental-processes'],
            'behavioral': ['behavior-modification', 'learning-theory', 'conditioning'],
            'social': ['social-psychology', 'group-dynamics', 'interpersonal-skills'],
            'developmental': ['lifespan-development', 'stage-theories', 'growth-mindset']
        },
        contentTypes: {
            'educational': ['courses', 'workshops', 'self-help-materials'],
            'therapeutic': ['interventions', 'techniques', 'protocols'],
            'assessment': ['questionnaires', 'scales', 'diagnostic-tools'],
            'research': ['studies', 'methodologies', 'frameworks']
        },
        culturalConsiderations: ['diversity', 'inclusion', 'cultural-adaptation', 'language-sensitivity'],
        ethicalGuidelines: ['informed-consent', 'confidentiality', 'do-no-harm', 'professional-boundaries']
    },

    'clinical-psychology': {
        name: 'Clinical Psychology',
        description: 'Assessment, diagnosis, and treatment of mental health conditions',
        requirements: [
            'clinical-evidence-base',
            'diagnostic-accuracy',
            'safety-protocols',
            'ethical-standards',
            'professional-oversight',
            'risk-assessment',
            'contraindication-awareness'
        ],
        validation: [
            'clinical-validity',
            'safety-assessment',
            'evidence-quality',
            'professional-standards',
            'regulatory-compliance'
        ],
        approaches: [
            'cognitive-behavioral-therapy',
            'psychodynamic',
            'humanistic-therapy',
            'integrative-therapy',
            'evidence-based-treatments'
        ],
        integrationStrategy: 'clinical-protocols',
        qualityThreshold: 0.95,
        preferredAgents: ['research', 'clinical-expert', 'test-generator', 'psychometrician', 'quality-guardian'],
        specializations: {
            'assessment': ['psychological-testing', 'diagnostic-interviews', 'behavioral-observation'],
            'therapy': ['individual-therapy', 'group-therapy', 'family-therapy'],
            'disorders': ['anxiety-disorders', 'mood-disorders', 'personality-disorders', 'trauma-ptsd'],
            'populations': ['children-adolescents', 'adults', 'elderly', 'couples-families']
        },
        contentTypes: {
            'assessment-tools': ['diagnostic-interviews', 'psychological-tests', 'rating-scales'],
            'treatment-protocols': ['therapy-manuals', 'intervention-guides', 'session-plans'],
            'psychoeducation': ['patient-education', 'family-resources', 'self-help-materials'],
            'professional-training': ['clinical-supervision', 'competency-frameworks', 'ethics-training']
        },
        safetyRequirements: ['suicide-risk-assessment', 'crisis-intervention', 'mandatory-reporting'],
        professionalStandards: ['APA-guidelines', 'licensing-requirements', 'continuing-education'],
        researchBase: ['randomized-controlled-trials', 'meta-analyses', 'clinical-guidelines']
    },

    'educational-psychology': {
        name: 'Educational Psychology',
        description: 'Psychology applied to learning, teaching, and educational contexts',
        requirements: [
            'learning-theory-foundation',
            'developmental-appropriateness',
            'individual-differences',
            'assessment-validity',
            'instructional-design',
            'technology-integration'
        ],
        validation: [
            'pedagogical-soundness',
            'learning-outcomes',
            'engagement-metrics',
            'accessibility-standards',
            'curriculum-alignment'
        ],
        approaches: [
            'constructivist-learning',
            'social-cognitive-theory',
            'multiple-intelligences',
            'competency-based-education',
            'personalized-learning'
        ],
        integrationStrategy: 'curriculum-alignment',
        qualityThreshold: 0.85,
        preferredAgents: ['research', 'pedagogy-expert', 'curriculum-designer', 'assessment-creator', 'quality-guardian'],
        specializations: {
            'learning-processes': ['cognitive-load', 'memory-retention', 'skill-acquisition'],
            'motivation': ['intrinsic-motivation', 'goal-setting', 'self-regulation'],
            'assessment': ['formative-assessment', 'summative-assessment', 'authentic-assessment'],
            'special-needs': ['learning-disabilities', 'gifted-education', 'inclusive-education']
        },
        contentTypes: {
            'curriculum': ['course-design', 'lesson-plans', 'learning-modules'],
            'assessment': ['rubrics', 'portfolios', 'performance-tasks'],
            'instruction': ['teaching-strategies', 'classroom-management', 'technology-tools'],
            'student-support': ['study-skills', 'academic-coaching', 'learning-strategies']
        },
        ageGroups: ['early-childhood', 'elementary', 'middle-school', 'high-school', 'adult-learners'],
        learningEnvironments: ['traditional-classroom', 'online-learning', 'hybrid-models', 'workplace-training'],
        assessmentPrinciples: ['validity', 'reliability', 'fairness', 'transparency']
    },

    'organizational-psychology': {
        name: 'Organizational Psychology',
        description: 'Psychology applied to workplace behavior and organizational effectiveness',
        requirements: [
            'organizational-context',
            'stakeholder-analysis',
            'change-management',
            'business-alignment',
            'roi-consideration',
            'implementation-feasibility'
        ],
        validation: [
            'organizational-fit',
            'business-impact',
            'implementation-viability',
            'stakeholder-acceptance',
            'sustainability'
        ],
        approaches: [
            'systems-thinking',
            'positive-psychology',
            'behavioral-economics',
            'change-management-models',
            'evidence-based-management'
        ],
        integrationStrategy: 'organizational-systems',
        qualityThreshold: 0.85,
        preferredAgents: ['research', 'organizational-expert', 'change-management', 'architect', 'quality-guardian'],
        specializations: {
            'leadership': ['leadership-development', 'executive-coaching', 'succession-planning'],
            'teams': ['team-dynamics', 'collaboration', 'conflict-resolution'],
            'culture': ['organizational-culture', 'values-alignment', 'culture-change'],
            'performance': ['performance-management', 'goal-setting', 'feedback-systems']
        },
        contentTypes: {
            'assessments': ['360-feedback', 'culture-surveys', 'engagement-assessments'],
            'interventions': ['training-programs', 'coaching-protocols', 'change-initiatives'],
            'frameworks': ['competency-models', 'leadership-frameworks', 'culture-frameworks'],
            'tools': ['diagnostic-tools', 'planning-templates', 'measurement-systems']
        },
        organizationalLevels: ['individual', 'team', 'department', 'organization', 'multi-organization'],
        businessFunctions: ['hr', 'management', 'sales', 'customer-service', 'operations'],
        implementationConsiderations: ['budget-constraints', 'time-limitations', 'resource-availability']
    },

    'health-psychology': {
        name: 'Health Psychology',
        description: 'Psychology applied to health, illness, and healthcare',
        requirements: [
            'medical-knowledge-base',
            'health-behavior-theory',
            'patient-centered-approach',
            'evidence-based-interventions',
            'interdisciplinary-collaboration',
            'cultural-competence'
        ],
        validation: [
            'health-outcomes',
            'behavior-change-effectiveness',
            'patient-satisfaction',
            'clinical-integration',
            'safety-considerations'
        ],
        approaches: [
            'biopsychosocial-model',
            'transtheoretical-model',
            'health-belief-model',
            'social-cognitive-theory',
            'motivational-interviewing'
        ],
        integrationStrategy: 'healthcare-integration',
        qualityThreshold: 0.90,
        preferredAgents: ['research', 'health-expert', 'clinical-expert', 'nlp-generator', 'quality-guardian'],
        specializations: {
            'prevention': ['primary-prevention', 'secondary-prevention', 'risk-reduction'],
            'chronic-illness': ['diabetes-management', 'cardiac-rehabilitation', 'pain-management'],
            'behavior-change': ['smoking-cessation', 'weight-management', 'exercise-promotion'],
            'mental-health': ['stress-management', 'anxiety-reduction', 'depression-prevention']
        },
        contentTypes: {
            'interventions': ['behavior-change-programs', 'stress-reduction', 'wellness-coaching'],
            'education': ['health-literacy', 'patient-education', 'prevention-programs'],
            'assessment': ['health-behavior-assessments', 'quality-of-life-measures', 'stress-measures'],
            'support': ['support-groups', 'peer-programs', 'family-interventions']
        },
        healthConditions: ['cardiovascular', 'diabetes', 'cancer', 'chronic-pain', 'mental-health'],
        populations: ['pediatric', 'adult', 'elderly', 'chronic-illness', 'caregivers'],
        settingsContexts: ['hospitals', 'clinics', 'community-health', 'workplace-wellness', 'telehealth']
    },

    'positive-psychology': {
        name: 'Positive Psychology',
        description: 'Focus on human strengths, well-being, and flourishing',
        requirements: [
            'strengths-based-approach',
            'well-being-focus',
            'positive-interventions',
            'character-development',
            'meaning-purpose',
            'resilience-building'
        ],
        validation: [
            'well-being-outcomes',
            'strengths-development',
            'life-satisfaction',
            'engagement-levels',
            'resilience-measures'
        ],
        approaches: [
            'perma-model',
            'via-character-strengths',
            'mindfulness-based',
            'gratitude-practices',
            'flow-theory'
        ],
        integrationStrategy: 'holistic-wellbeing',
        qualityThreshold: 0.80,
        preferredAgents: ['research', 'wellness-expert', 'technique-designer', 'nlp-generator', 'quality-guardian'],
        specializations: {
            'well-being': ['life-satisfaction', 'happiness', 'flourishing', 'eudaimonia'],
            'strengths': ['character-strengths', 'talent-development', 'strengths-identification'],
            'resilience': ['stress-resilience', 'post-traumatic-growth', 'coping-strategies'],
            'relationships': ['positive-relationships', 'social-connections', 'empathy-building']
        },
        contentTypes: {
            'assessments': ['strengths-assessments', 'well-being-measures', 'values-clarification'],
            'interventions': ['gratitude-practices', 'mindfulness-exercises', 'strengths-development'],
            'programs': ['happiness-programs', 'resilience-training', 'meaning-making'],
            'tools': ['journaling-prompts', 'reflection-exercises', 'goal-setting-frameworks']
        },
        wellBeingDomains: ['emotional', 'psychological', 'social', 'physical', 'spiritual'],
        applicationAreas: ['education', 'workplace', 'healthcare', 'community', 'personal-development'],
        measurementFocus: ['subjective-well-being', 'psychological-capital', 'character-strengths']
    },

    'developmental-psychology': {
        name: 'Developmental Psychology',
        description: 'Psychological development across the lifespan',
        requirements: [
            'developmental-stages',
            'age-appropriateness',
            'individual-differences',
            'contextual-factors',
            'longitudinal-perspective',
            'family-systems'
        ],
        validation: [
            'developmental-accuracy',
            'age-appropriateness',
            'individual-variation',
            'cultural-relevance',
            'family-integration'
        ],
        approaches: [
            'stage-theories',
            'ecological-systems',
            'attachment-theory',
            'social-learning-theory',
            'cognitive-development'
        ],
        integrationStrategy: 'developmental-progression',
        qualityThreshold: 0.85,
        preferredAgents: ['research', 'development-expert', 'family-specialist', 'assessment-creator', 'quality-guardian'],
        specializations: {
            'cognitive': ['piaget-theory', 'information-processing', 'executive-functions'],
            'social-emotional': ['attachment', 'emotional-regulation', 'social-skills'],
            'physical': ['motor-development', 'brain-development', 'health-development'],
            'moral': ['moral-reasoning', 'values-development', 'character-formation']
        },
        contentTypes: {
            'assessments': ['developmental-screenings', 'milestone-checklists', 'readiness-assessments'],
            'interventions': ['early-intervention', 'developmental-support', 'family-guidance'],
            'education': ['parenting-education', 'child-development', 'adolescent-programs'],
            'support': ['family-support', 'caregiver-training', 'transition-support']
        },
        lifeStages: ['prenatal', 'infancy', 'early-childhood', 'school-age', 'adolescence', 'adulthood', 'aging'],
        contexts: ['family', 'school', 'peer-groups', 'community', 'culture'],
        riskProtectiveFactors: ['risk-assessment', 'protective-factors', 'resilience-promotion']
    },

    'social-psychology': {
        name: 'Social Psychology',
        description: 'How people think, feel, and behave in social contexts',
        requirements: [
            'social-context-awareness',
            'group-dynamics',
            'cultural-sensitivity',
            'interpersonal-processes',
            'social-influence',
            'diversity-inclusion'
        ],
        validation: [
            'social-validity',
            'group-effectiveness',
            'interpersonal-outcomes',
            'cultural-appropriateness',
            'social-impact'
        ],
        approaches: [
            'social-identity-theory',
            'social-learning-theory',
            'attribution-theory',
            'social-cognition',
            'intergroup-contact'
        ],
        integrationStrategy: 'social-systems',
        qualityThreshold: 0.80,
        preferredAgents: ['research', 'social-expert', 'group-facilitator', 'diversity-specialist', 'quality-guardian'],
        specializations: {
            'groups': ['group-dynamics', 'team-building', 'leadership', 'conflict-resolution'],
            'attitudes': ['attitude-change', 'persuasion', 'stereotypes', 'prejudice-reduction'],
            'relationships': ['interpersonal-attraction', 'close-relationships', 'social-support'],
            'influence': ['conformity', 'compliance', 'obedience', 'social-norms']
        },
        contentTypes: {
            'training': ['diversity-training', 'leadership-development', 'communication-skills'],
            'interventions': ['prejudice-reduction', 'conflict-resolution', 'team-building'],
            'assessments': ['social-skills-assessment', 'group-climate', 'interpersonal-measures'],
            'programs': ['social-skills-training', 'cultural-competence', 'inclusion-programs']
        },
        socialContexts: ['workplace', 'educational', 'community', 'family', 'peer-groups'],
        diversityDimensions: ['race-ethnicity', 'gender', 'age', 'religion', 'sexual-orientation', 'disability'],
        applicationAreas: ['organizational', 'educational', 'legal', 'health', 'community']
    },

    'cognitive-psychology': {
        name: 'Cognitive Psychology',
        description: 'Mental processes including thinking, memory, perception, and problem-solving',
        requirements: [
            'cognitive-theory-base',
            'information-processing',
            'empirical-evidence',
            'cognitive-assessment',
            'brain-behavior-connections',
            'individual-differences'
        ],
        validation: [
            'cognitive-validity',
            'information-processing-accuracy',
            'transfer-effectiveness',
            'ecological-validity',
            'measurement-precision'
        ],
        approaches: [
            'information-processing-model',
            'cognitive-load-theory',
            'dual-coding-theory',
            'metacognitive-strategies',
            'embodied-cognition'
        ],
        integrationStrategy: 'cognitive-frameworks',
        qualityThreshold: 0.85,
        preferredAgents: ['research', 'cognitive-expert', 'neuropsych-specialist', 'assessment-creator', 'quality-guardian'],
        specializations: {
            'memory': ['working-memory', 'long-term-memory', 'episodic-memory', 'semantic-memory'],
            'attention': ['selective-attention', 'divided-attention', 'sustained-attention'],
            'executive': ['cognitive-control', 'planning', 'inhibition', 'cognitive-flexibility'],
            'language': ['language-processing', 'reading-comprehension', 'verbal-reasoning']
        },
        contentTypes: {
            'assessments': ['cognitive-batteries', 'memory-tests', 'attention-measures', 'executive-assessments'],
            'training': ['cognitive-training', 'memory-strategies', 'attention-training', 'problem-solving'],
            'interventions': ['cognitive-remediation', 'strategy-instruction', 'metacognitive-training'],
            'tools': ['cognitive-aids', 'memory-supports', 'attention-tools', 'thinking-frameworks']
        },
        cognitiveProcesses: ['perception', 'attention', 'memory', 'language', 'thinking', 'problem-solving'],
        applications: ['education', 'rehabilitation', 'training', 'user-interface-design', 'decision-making'],
        populations: ['typical-development', 'learning-disabilities', 'brain-injury', 'aging', 'gifted']
    },

    // === Specialized Application Domains ===
    'sports-psychology': {
        name: 'Sports Psychology',
        description: 'Psychology applied to athletic performance and sports participation',
        requirements: [
            'performance-psychology',
            'motivation-theory',
            'stress-management',
            'team-dynamics',
            'skill-acquisition',
            'mental-training'
        ],
        validation: [
            'performance-outcomes',
            'athlete-satisfaction',
            'skill-development',
            'mental-toughness',
            'team-cohesion'
        ],
        approaches: [
            'cognitive-behavioral-techniques',
            'mindfulness-based-performance',
            'goal-setting-theory',
            'self-determination-theory',
            'flow-theory'
        ],
        integrationStrategy: 'performance-optimization',
        qualityThreshold: 0.80,
        preferredAgents: ['research', 'sports-expert', 'performance-coach', 'mental-skills-trainer', 'quality-guardian'],
        specializations: {
            'performance': ['peak-performance', 'choking-prevention', 'flow-states', 'confidence-building'],
            'mental-skills': ['visualization', 'self-talk', 'concentration', 'arousal-regulation'],
            'team': ['team-cohesion', 'leadership', 'communication', 'group-dynamics'],
            'lifestyle': ['injury-recovery', 'career-transitions', 'life-balance', 'retirement']
        },
        applicationAreas: ['individual-sports', 'team-sports', 'youth-sports', 'elite-athletes', 'recreational-athletes'],
        interventionTypes: ['mental-skills-training', 'performance-counseling', 'team-building', 'lifestyle-management']
    },

    'forensic-psychology': {
        name: 'Forensic Psychology',
        description: 'Psychology applied to legal and criminal justice contexts',
        requirements: [
            'legal-knowledge',
            'ethical-standards',
            'assessment-validity',
            'expert-testimony',
            'risk-assessment',
            'cultural-competence'
        ],
        validation: [
            'legal-relevance',
            'psychometric-standards',
            'ethical-compliance',
            'admissibility-criteria',
            'professional-standards'
        ],
        approaches: [
            'risk-assessment-models',
            'therapeutic-jurisprudence',
            'restorative-justice',
            'evidence-based-practice',
            'trauma-informed-care'
        ],
        integrationStrategy: 'legal-compliance',
        qualityThreshold: 0.95,
        preferredAgents: ['research', 'forensic-expert', 'legal-specialist', 'risk-assessor', 'quality-guardian'],
        specializations: {
            'assessment': ['competency-evaluation', 'risk-assessment', 'psychological-evaluation'],
            'treatment': ['offender-rehabilitation', 'victim-services', 'trauma-treatment'],
            'consultation': ['jury-selection', 'witness-preparation', 'legal-consultation'],
            'research': ['eyewitness-memory', 'decision-making', 'criminal-behavior']
        },
        legalContexts: ['criminal-court', 'civil-court', 'family-court', 'correctional-settings'],
        ethicalConsiderations: ['dual-relationships', 'confidentiality-limits', 'informed-consent', 'competence-boundaries']
    }
};

// === Domain Utility Functions ===
const domainUtilities = {
    /**
     * Get domain configuration by name
     */
    getDomain(domainName) {
        return domainSettings[domainName] || domainSettings['general-psychology'];
    },

    /**
     * Get all available domains
     */
    getAllDomains() {
        return Object.keys(domainSettings);
    },

    /**
     * Get domains by category
     */
    getDomainsByCategory(category) {
        const categories = {
            'core': ['general-psychology', 'clinical-psychology', 'educational-psychology', 'organizational-psychology'],
            'applied': ['health-psychology', 'sports-psychology', 'forensic-psychology'],
            'theoretical': ['cognitive-psychology', 'social-psychology', 'developmental-psychology', 'positive-psychology']
        };

        return categories[category] || [];
    },

    /**
     * Find best matching domain for content requirements
     */
    findBestDomain(requirements) {
        let bestMatch = 'general-psychology';
        let bestScore = 0;

        Object.entries(domainSettings).forEach(([domainName, config]) => {
            const matchScore = this.calculateDomainMatch(requirements, config);
            if (matchScore > bestScore) {
                bestScore = matchScore;
                bestMatch = domainName;
            }
        });

        return { domain: bestMatch, confidence: bestScore };
    },

    /**
     * Calculate domain match score
     */
    calculateDomainMatch(requirements, domainConfig) {
        const requirementMatches = requirements.filter(req =>
            domainConfig.requirements.includes(req) ||
            domainConfig.approaches.some(approach => approach.includes(req.toLowerCase())) ||
            Object.values(domainConfig.specializations || {}).flat().includes(req)
        );

        return requirementMatches.length / requirements.length;
    },

    /**
     * Get recommended agent configuration for domain
     */
    getRecommendedAgents(domainName, complexity = 'standard') {
        const domain = this.getDomain(domainName);
        const baseAgents = domain.preferredAgents || ['research', 'domain-expert', 'quality-guardian'];

        // Adjust based on complexity
        const complexityAdjustments = {
            'minimal': (agents) => agents.slice(0, 3),
            'standard': (agents) => agents,
            'comprehensive': (agents) => [...agents, 'integrator', 'peer-reviewer'],
            'expert': (agents) => [...agents, 'integrator', 'peer-reviewer', 'senior-expert']
        };

        return complexityAdjustments[complexity] ? complexityAdjustments[complexity](baseAgents) : baseAgents;
    },

    /**
     * Validate content against domain requirements
     */
    validateDomainCompliance(content, domainName) {
        const domain = this.getDomain(domainName);
        const validationResults = {
            passed: true,
            score: 0,
            issues: [],
            recommendations: []
        };

        // Check each validation criterion
        domain.validation.forEach(criterion => {
            const check = this.checkValidationCriterion(content, criterion, domain);
            validationResults.score += check.score;

            if (!check.passed) {
                validationResults.passed = false;
                validationResults.issues.push(check.issue);
                validationResults.recommendations.push(check.recommendation);
            }
        });

        validationResults.score = validationResults.score / domain.validation.length;
        return validationResults;
    },

    /**
     * Check individual validation criterion
     */
    checkValidationCriterion(content, criterion, domain) {
        // This would be implemented with specific validation logic
        // For now, return a mock validation
        return {
            passed: Math.random() > 0.2, // 80% pass rate for simulation
            score: Math.random(),
            issue: `Content may not meet ${criterion} requirements`,
            recommendation: `Review content for ${criterion} compliance`
        };
    },

    /**
     * Get cultural considerations for domain
     */
    getCulturalConsiderations(domainName) {
        const domain = this.getDomain(domainName);
        return domain.culturalConsiderations || ['diversity', 'inclusion', 'cultural-adaptation'];
    },

    /**
     * Get ethical guidelines for domain
     */
    getEthicalGuidelines(domainName) {
        const domain = this.getDomain(domainName);
        return domain.ethicalGuidelines || ['informed-consent', 'confidentiality', 'do-no-harm'];
    },

    /**
     * Generate domain-specific quality metrics
     */
    generateQualityMetrics(domainName) {
        const domain = this.getDomain(domainName);
        return {
            threshold: domain.qualityThreshold,
            validation: domain.validation,
            approaches: domain.approaches,
            requirements: domain.requirements
        };
    }
};

module.exports = {
    domainSettings,
    domainUtilities
};