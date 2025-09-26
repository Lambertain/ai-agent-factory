/**
 * Agent Configurations - Universal agent definitions and mappings
 * Configurable agent system for different psychological domains and content types
 */

const agentConfigs = {
    // Content type to agent mapping for dynamic workflow creation
    contentTypeMapping: {
        'therapeutic-program': ['research', 'architect', 'test-generator', 'nlp-generator', 'quality-guardian'],
        'assessment-tool': ['research', 'test-generator', 'psychometrician', 'quality-guardian'],
        'technique-library': ['research', 'technique-designer', 'nlp-generator', 'quality-guardian'],
        'intervention-protocol': ['research', 'clinical-expert', 'architect', 'nlp-generator', 'quality-guardian'],
        'educational-curriculum': ['research', 'pedagogy-expert', 'curriculum-designer', 'assessment-creator', 'quality-guardian'],
        'organizational-framework': ['research', 'organizational-expert', 'architect', 'change-management', 'quality-guardian'],
        'research-methodology': ['research-methodologist', 'statistical-analyst', 'design-expert', 'quality-guardian'],
        'wellness-program': ['wellness-expert', 'technique-designer', 'nlp-generator', 'lifestyle-coach', 'quality-guardian'],
        'comprehensive-program': ['research', 'domain-expert', 'architect', 'nlp-generator', 'test-generator', 'integrator', 'quality-guardian'],
        'refinement': ['quality-guardian', 'content-editor', 'domain-expert'],
        'custom': [] // Will be determined dynamically
    },

    // Detailed agent definitions with capabilities and configurations
    agentDefinitions: {
        // === Core Research and Analysis Agents ===
        'research': {
            name: 'Research Agent',
            description: 'Conducts literature reviews and evidence synthesis',
            capabilities: [
                'literature-review',
                'evidence-synthesis',
                'meta-analysis',
                'research-validation',
                'source-evaluation',
                'bibliography-creation'
            ],
            specializations: ['evidence-based-practice', 'systematic-reviews', 'research-methodology'],
            outputTypes: ['research-report', 'evidence-summary', 'literature-matrix', 'recommendations'],
            processingTime: {
                simple: 60000,      // 1 minute
                moderate: 120000,   // 2 minutes
                complex: 300000     // 5 minutes
            },
            qualityMetrics: ['evidence-quality', 'source-reliability', 'comprehensiveness'],
            ragIntegration: true,
            concurrencyLimit: 3,
            dependencies: []
        },

        'domain-expert': {
            name: 'Domain Expert Agent',
            description: 'Provides specialized domain knowledge and validation',
            capabilities: [
                'domain-expertise',
                'specialized-knowledge',
                'expert-validation',
                'best-practices',
                'standards-compliance'
            ],
            specializations: [], // Dynamically populated based on domain
            outputTypes: ['expert-review', 'domain-analysis', 'recommendations', 'validation-report'],
            processingTime: {
                simple: 90000,
                moderate: 180000,
                complex: 360000
            },
            qualityMetrics: ['expertise-depth', 'accuracy', 'practical-applicability'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research']
        },

        // === Design and Architecture Agents ===
        'architect': {
            name: 'Program Architect Agent',
            description: 'Designs overall structure and framework of psychological programs',
            capabilities: [
                'system-design',
                'framework-development',
                'modular-architecture',
                'integration-planning',
                'scalability-design'
            ],
            specializations: ['cognitive-frameworks', 'behavioral-models', 'learning-architectures'],
            outputTypes: ['program-blueprint', 'module-structure', 'integration-plan', 'framework-design'],
            processingTime: {
                simple: 120000,
                moderate: 240000,
                complex: 480000
            },
            qualityMetrics: ['structural-coherence', 'modularity', 'scalability'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research', 'domain-expert']
        },

        'curriculum-designer': {
            name: 'Curriculum Designer Agent',
            description: 'Creates educational structures and learning progressions',
            capabilities: [
                'curriculum-development',
                'learning-progression',
                'competency-mapping',
                'outcome-alignment',
                'pedagogical-sequencing'
            ],
            specializations: ['adult-learning', 'skill-development', 'competency-based-design'],
            outputTypes: ['curriculum-outline', 'learning-modules', 'progression-map', 'competency-framework'],
            processingTime: {
                simple: 150000,
                moderate: 300000,
                complex: 600000
            },
            qualityMetrics: ['learning-alignment', 'progression-logic', 'outcome-clarity'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research', 'pedagogy-expert']
        },

        // === Assessment and Testing Agents ===
        'test-generator': {
            name: 'Assessment Generator Agent',
            description: 'Creates psychological assessments and diagnostic tools',
            capabilities: [
                'test-development',
                'item-generation',
                'scale-construction',
                'validation-design',
                'scoring-systems'
            ],
            specializations: ['psychometrics', 'clinical-assessment', 'personality-testing', 'cognitive-assessment'],
            outputTypes: ['assessment-battery', 'questionnaire', 'diagnostic-tool', 'scoring-rubric'],
            processingTime: {
                simple: 180000,
                moderate: 360000,
                complex: 720000
            },
            qualityMetrics: ['reliability', 'validity', 'usability', 'clinical-utility'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research', 'psychometrician']
        },

        'psychometrician': {
            name: 'Psychometric Specialist Agent',
            description: 'Ensures statistical validity and reliability of assessments',
            capabilities: [
                'psychometric-analysis',
                'reliability-testing',
                'validity-assessment',
                'factor-analysis',
                'norm-development'
            ],
            specializations: ['classical-test-theory', 'item-response-theory', 'factor-analysis'],
            outputTypes: ['psychometric-report', 'reliability-analysis', 'validity-study', 'normative-data'],
            processingTime: {
                simple: 120000,
                moderate: 300000,
                complex: 600000
            },
            qualityMetrics: ['statistical-rigor', 'measurement-precision', 'interpretability'],
            ragIntegration: false,
            concurrencyLimit: 1,
            dependencies: ['test-generator']
        },

        // === Content Generation Agents ===
        'nlp-generator': {
            name: 'NLP Content Generator Agent',
            description: 'Generates therapeutic language patterns and techniques',
            capabilities: [
                'language-pattern-generation',
                'therapeutic-scripting',
                'content-adaptation',
                'personalization',
                'multi-modal-content'
            ],
            specializations: ['therapeutic-language', 'behavior-change-messaging', 'motivational-content'],
            outputTypes: ['therapeutic-scripts', 'guided-exercises', 'affirmations', 'behavioral-prompts'],
            processingTime: {
                simple: 90000,
                moderate: 180000,
                complex: 360000
            },
            qualityMetrics: ['language-appropriateness', 'therapeutic-efficacy', 'engagement-potential'],
            ragIntegration: true,
            concurrencyLimit: 4,
            dependencies: ['research', 'technique-designer']
        },

        'technique-designer': {
            name: 'Technique Designer Agent',
            description: 'Creates specific therapeutic and behavioral techniques',
            capabilities: [
                'technique-development',
                'intervention-design',
                'exercise-creation',
                'protocol-development',
                'adaptation-strategies'
            ],
            specializations: ['cognitive-techniques', 'behavioral-interventions', 'mindfulness-practices'],
            outputTypes: ['technique-library', 'exercise-protocols', 'intervention-guides', 'practice-sheets'],
            processingTime: {
                simple: 120000,
                moderate: 240000,
                complex: 480000
            },
            qualityMetrics: ['technique-effectiveness', 'implementation-clarity', 'user-engagement'],
            ragIntegration: true,
            concurrencyLimit: 3,
            dependencies: ['research', 'domain-expert']
        },

        // === Quality and Integration Agents ===
        'quality-guardian': {
            name: 'Quality Assurance Agent',
            description: 'Validates content quality and adherence to standards',
            capabilities: [
                'quality-assessment',
                'standards-validation',
                'content-review',
                'compliance-checking',
                'improvement-recommendations'
            ],
            specializations: ['clinical-standards', 'educational-standards', 'ethical-guidelines'],
            outputTypes: ['quality-report', 'compliance-checklist', 'improvement-plan', 'validation-certificate'],
            processingTime: {
                simple: 60000,
                moderate: 120000,
                complex: 240000
            },
            qualityMetrics: ['thoroughness', 'accuracy', 'standards-adherence'],
            ragIntegration: true,
            concurrencyLimit: 5,
            dependencies: []
        },

        'integrator': {
            name: 'Content Integration Agent',
            description: 'Synthesizes and integrates outputs from multiple agents',
            capabilities: [
                'content-synthesis',
                'integration-management',
                'coherence-optimization',
                'format-standardization',
                'cross-reference-creation'
            ],
            specializations: ['content-architecture', 'information-design', 'user-experience'],
            outputTypes: ['integrated-program', 'unified-content', 'cross-referenced-materials', 'final-package'],
            processingTime: {
                simple: 180000,
                moderate: 360000,
                complex: 720000
            },
            qualityMetrics: ['integration-quality', 'coherence', 'usability'],
            ragIntegration: false,
            concurrencyLimit: 1,
            dependencies: ['nlp-generator', 'technique-designer', 'test-generator']
        },

        // === Specialized Domain Experts ===
        'clinical-expert': {
            name: 'Clinical Psychology Expert',
            description: 'Provides clinical psychology expertise and validation',
            capabilities: [
                'clinical-assessment',
                'therapeutic-validation',
                'evidence-based-practice',
                'ethical-review',
                'safety-assessment'
            ],
            specializations: ['psychotherapy', 'clinical-assessment', 'mental-health', 'evidence-based-treatment'],
            outputTypes: ['clinical-review', 'safety-assessment', 'therapeutic-recommendations', 'contraindications'],
            processingTime: {
                simple: 120000,
                moderate: 300000,
                complex: 600000
            },
            qualityMetrics: ['clinical-accuracy', 'safety', 'ethical-compliance'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research']
        },

        'pedagogy-expert': {
            name: 'Educational Psychology Expert',
            description: 'Applies learning theory and educational psychology principles',
            capabilities: [
                'learning-theory-application',
                'educational-design',
                'assessment-strategy',
                'motivation-enhancement',
                'accessibility-optimization'
            ],
            specializations: ['adult-learning', 'cognitive-load-theory', 'motivation-theory', 'learning-styles'],
            outputTypes: ['pedagogical-framework', 'learning-strategy', 'assessment-plan', 'motivation-design'],
            processingTime: {
                simple: 90000,
                moderate: 180000,
                complex: 360000
            },
            qualityMetrics: ['pedagogical-soundness', 'learning-effectiveness', 'engagement'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research']
        },

        'organizational-expert': {
            name: 'Organizational Psychology Expert',
            description: 'Applies organizational psychology to workplace interventions',
            capabilities: [
                'organizational-analysis',
                'workplace-intervention',
                'change-management',
                'team-dynamics',
                'leadership-development'
            ],
            specializations: ['organizational-behavior', 'workplace-wellbeing', 'leadership-psychology'],
            outputTypes: ['organizational-assessment', 'intervention-strategy', 'implementation-plan', 'change-roadmap'],
            processingTime: {
                simple: 120000,
                moderate: 300000,
                complex: 600000
            },
            qualityMetrics: ['organizational-fit', 'implementation-feasibility', 'business-alignment'],
            ragIntegration: true,
            concurrencyLimit: 2,
            dependencies: ['research']
        },

        // === Supporting Specialist Agents ===
        'statistical-analyst': {
            name: 'Statistical Analysis Agent',
            description: 'Provides statistical analysis and research methodology support',
            capabilities: [
                'statistical-analysis',
                'research-design',
                'data-interpretation',
                'effect-size-calculation',
                'power-analysis'
            ],
            specializations: ['experimental-design', 'statistical-modeling', 'meta-analysis'],
            outputTypes: ['statistical-plan', 'analysis-results', 'interpretation-report', 'methodology-review'],
            processingTime: {
                simple: 90000,
                moderate: 180000,
                complex: 360000
            },
            qualityMetrics: ['statistical-rigor', 'methodological-soundness', 'interpretability'],
            ragIntegration: false,
            concurrencyLimit: 2,
            dependencies: []
        },

        'content-editor': {
            name: 'Content Editor Agent',
            description: 'Refines and polishes content for clarity and engagement',
            capabilities: [
                'content-editing',
                'clarity-optimization',
                'engagement-enhancement',
                'accessibility-improvement',
                'format-standardization'
            ],
            specializations: ['technical-writing', 'educational-content', 'therapeutic-materials'],
            outputTypes: ['edited-content', 'style-guide', 'accessibility-report', 'engagement-analysis'],
            processingTime: {
                simple: 60000,
                moderate: 120000,
                complex: 240000
            },
            qualityMetrics: ['readability', 'clarity', 'engagement', 'accessibility'],
            ragIntegration: false,
            concurrencyLimit: 3,
            dependencies: []
        }
    },

    // Agent role hierarchies and dependencies
    agentHierarchy: {
        'senior-agents': ['research', 'domain-expert', 'clinical-expert', 'architect'],
        'specialist-agents': ['psychometrician', 'statistical-analyst', 'pedagogy-expert', 'organizational-expert'],
        'generation-agents': ['nlp-generator', 'technique-designer', 'test-generator', 'curriculum-designer'],
        'integration-agents': ['integrator', 'quality-guardian', 'content-editor'],
        'support-agents': ['content-editor', 'statistical-analyst']
    },

    // Default agent selection for different scenarios
    defaultSelections: {
        'minimal': ['research', 'nlp-generator', 'quality-guardian'],
        'standard': ['research', 'architect', 'nlp-generator', 'test-generator', 'quality-guardian'],
        'comprehensive': ['research', 'domain-expert', 'architect', 'test-generator', 'nlp-generator', 'technique-designer', 'integrator', 'quality-guardian'],
        'clinical': ['research', 'clinical-expert', 'test-generator', 'nlp-generator', 'quality-guardian'],
        'educational': ['research', 'pedagogy-expert', 'curriculum-designer', 'assessment-creator', 'quality-guardian'],
        'organizational': ['research', 'organizational-expert', 'architect', 'change-management', 'quality-guardian']
    },

    // Quality thresholds for different agent types
    qualityThresholds: {
        'research': 0.85,
        'test-generator': 0.90,
        'clinical-expert': 0.95,
        'quality-guardian': 0.80,
        'nlp-generator': 0.75,
        'technique-designer': 0.80,
        'architect': 0.85,
        'integrator': 0.80,
        'default': 0.80
    },

    // Load balancing and performance optimization
    performanceSettings: {
        maxConcurrentAgents: 8,
        taskTimeout: 600000, // 10 minutes
        retryLimit: 3,
        retryDelay: 5000,
        loadBalancingStrategy: 'best-fit', // 'round-robin', 'least-loaded', 'best-performance', 'specialized', 'best-fit'
        priorityQueuing: true,
        adaptivePriority: true
    },

    // Agent communication and coordination patterns
    coordinationPatterns: {
        'sequential': {
            description: 'Agents work in sequence, each using previous outputs',
            suitable: ['research -> architect -> generator -> quality'],
            advantages: ['clear dependencies', 'building complexity'],
            disadvantages: ['longer execution time']
        },
        'parallel': {
            description: 'Multiple agents work simultaneously on different aspects',
            suitable: ['multiple generators', 'multiple experts'],
            advantages: ['faster execution', 'diverse perspectives'],
            disadvantages: ['integration complexity']
        },
        'hierarchical': {
            description: 'Senior agents coordinate junior agents',
            suitable: ['complex projects', 'quality-critical work'],
            advantages: ['quality control', 'expertise leveraging'],
            disadvantages: ['coordination overhead']
        },
        'collaborative': {
            description: 'Agents work together iteratively',
            suitable: ['refinement cycles', 'creative work'],
            advantages: ['high quality', 'creative solutions'],
            disadvantages: ['time intensive']
        }
    }
};

module.exports = agentConfigs;