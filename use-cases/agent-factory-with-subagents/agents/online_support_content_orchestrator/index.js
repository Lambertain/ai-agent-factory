/**
 * Psychology Content Orchestrator - Main Entry Point
 * Universal agent for coordinating psychological content creation through multi-agent systems
 *
 * @version 1.0.0
 * @author Psychology Content Orchestrator Team
 * @license MIT
 */

// Core modules
const PsychologyContentOrchestrator = require('./core/orchestrator');
const WorkflowManager = require('./core/workflow-manager');
const AgentDelegator = require('./core/agent-delegator');

// Configuration modules
const agentConfigs = require('./config/agent-configs');
const { domainSettings, domainUtilities } = require('./config/domain-settings');

// Integration modules
const RAGConnector = require('./integrations/rag-connector');
const ExternalAPIs = require('./integrations/external-apis');

// Utility modules
const ContentMerger = require('./utils/content-merger');
const QualityValidator = require('./utils/quality-validator');

// Examples and documentation
const usageExamples = require('./examples/usage-examples');

/**
 * Create a new Psychology Content Orchestrator instance with configuration
 * @param {Object} config - Configuration options
 * @returns {PsychologyContentOrchestrator} Configured orchestrator instance
 */
function createOrchestrator(config = {}) {
    return new PsychologyContentOrchestrator(config);
}

/**
 * Create orchestrator with preset domain configuration
 * @param {string} domain - Psychology domain name
 * @param {Object} additionalConfig - Additional configuration options
 * @returns {PsychologyContentOrchestrator} Domain-configured orchestrator
 */
function createDomainOrchestrator(domain, additionalConfig = {}) {
    const domainConfig = domainUtilities.getDomain(domain);

    return new PsychologyContentOrchestrator({
        domain,
        domainSettings: { [domain]: domainConfig },
        integrationStrategy: domainConfig.integrationStrategy || 'standard',
        qualityThreshold: domainConfig.qualityThreshold || 0.8,
        preferredAgents: domainConfig.preferredAgents || [],
        ...additionalConfig
    });
}

/**
 * Quick start methods for common use cases
 */
const QuickStart = {
    /**
     * Create clinical psychology orchestrator
     */
    clinical: (config = {}) => createDomainOrchestrator('clinical-psychology', {
        integrationStrategy: 'clinical-protocols',
        qualityThreshold: 0.9,
        strictMode: true,
        ...config
    }),

    /**
     * Create educational psychology orchestrator
     */
    educational: (config = {}) => createDomainOrchestrator('educational-psychology', {
        integrationStrategy: 'educational-curriculum',
        qualityThreshold: 0.85,
        ...config
    }),

    /**
     * Create organizational psychology orchestrator
     */
    organizational: (config = {}) => createDomainOrchestrator('organizational-psychology', {
        integrationStrategy: 'organizational-systems',
        qualityThreshold: 0.8,
        ...config
    }),

    /**
     * Create health psychology orchestrator
     */
    health: (config = {}) => createDomainOrchestrator('health-psychology', {
        integrationStrategy: 'healthcare-integration',
        qualityThreshold: 0.9,
        ...config
    }),

    /**
     * Create general psychology orchestrator
     */
    general: (config = {}) => createDomainOrchestrator('general-psychology', {
        integrationStrategy: 'standard',
        qualityThreshold: 0.8,
        ...config
    })
};

/**
 * Content type factory methods
 */
const ContentFactory = {
    /**
     * Create therapeutic program
     */
    async therapeuticProgram(orchestrator, description, options = {}) {
        return await orchestrator.createContent({
            type: 'therapeutic-program',
            description,
            domain: orchestrator.config.domain,
            ...options
        });
    },

    /**
     * Create assessment tool
     */
    async assessmentTool(orchestrator, description, options = {}) {
        return await orchestrator.createContent({
            type: 'assessment-tool',
            description,
            domain: orchestrator.config.domain,
            ...options
        });
    },

    /**
     * Create technique library
     */
    async techniqueLibrary(orchestrator, description, options = {}) {
        return await orchestrator.createContent({
            type: 'technique-library',
            description,
            domain: orchestrator.config.domain,
            ...options
        });
    },

    /**
     * Create comprehensive program
     */
    async comprehensiveProgram(orchestrator, description, options = {}) {
        return await orchestrator.createContent({
            type: 'comprehensive-program',
            description,
            domain: orchestrator.config.domain,
            ...options
        });
    },

    /**
     * Create intervention protocol
     */
    async interventionProtocol(orchestrator, description, options = {}) {
        return await orchestrator.createContent({
            type: 'intervention-protocol',
            description,
            domain: orchestrator.config.domain,
            ...options
        });
    }
};

/**
 * Utility functions for common operations
 */
const Utils = {
    /**
     * Validate configuration before creating orchestrator
     */
    validateConfig(config) {
        const errors = [];

        if (config.domain && !domainUtilities.getAllDomains().includes(config.domain)) {
            errors.push(`Unknown domain: ${config.domain}`);
        }

        if (config.qualityThreshold && (config.qualityThreshold < 0 || config.qualityThreshold > 1)) {
            errors.push('Quality threshold must be between 0 and 1');
        }

        if (config.integrationStrategy && !['standard', 'clinical-protocols', 'educational-curriculum', 'organizational-systems', 'holistic-wellbeing'].includes(config.integrationStrategy)) {
            errors.push(`Unknown integration strategy: ${config.integrationStrategy}`);
        }

        return {
            valid: errors.length === 0,
            errors
        };
    },

    /**
     * Get available domains
     */
    getAvailableDomains() {
        return domainUtilities.getAllDomains();
    },

    /**
     * Get domain configuration
     */
    getDomainConfig(domain) {
        return domainUtilities.getDomain(domain);
    },

    /**
     * Find best domain for requirements
     */
    findBestDomain(requirements) {
        return domainUtilities.findBestDomain(requirements);
    },

    /**
     * Get recommended agents for domain
     */
    getRecommendedAgents(domain, complexity = 'standard') {
        return domainUtilities.getRecommendedAgents(domain, complexity);
    }
};

/**
 * Integration helpers
 */
const Integrations = {
    /**
     * Create RAG-enabled orchestrator
     */
    withRAG: (config = {}) => createOrchestrator({
        ragEnabled: true,
        ragEndpoint: 'mcp__archon__rag_search_knowledge_base',
        relevanceThreshold: 0.7,
        defaultMatchCount: 5,
        ...config
    }),

    /**
     * Create Archon-integrated orchestrator
     */
    withArchon: (projectId, config = {}) => createOrchestrator({
        projectId,
        archonEnabled: true,
        externalAPIs: {
            archon: {
                enabled: true,
                endpoints: {
                    projects: 'find_projects',
                    tasks: 'find_tasks',
                    documents: 'find_documents'
                }
            }
        },
        ...config
    }),

    /**
     * Create GitHub-integrated orchestrator
     */
    withGitHub: (token, config = {}) => createOrchestrator({
        githubToken: token,
        githubIntegration: true,
        externalAPIs: {
            github: {
                enabled: true,
                token
            }
        },
        ...config
    })
};

// Main exports
module.exports = {
    // Core classes
    PsychologyContentOrchestrator,
    WorkflowManager,
    AgentDelegator,
    RAGConnector,
    ExternalAPIs,
    ContentMerger,
    QualityValidator,

    // Configuration
    agentConfigs,
    domainSettings,
    domainUtilities,

    // Factory methods
    createOrchestrator,
    createDomainOrchestrator,

    // Quick start presets
    QuickStart,

    // Content factory
    ContentFactory,

    // Utilities
    Utils,

    // Integrations
    Integrations,

    // Examples
    examples: usageExamples,

    // Version and metadata
    version: '1.0.0',
    name: 'Psychology Content Orchestrator',
    description: 'Universal agent for coordinating psychological content creation through multi-agent systems'
};

// Default export is the main orchestrator class
module.exports.default = PsychologyContentOrchestrator;