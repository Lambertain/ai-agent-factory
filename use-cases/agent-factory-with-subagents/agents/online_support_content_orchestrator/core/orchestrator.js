/**
 * Psychology Content Orchestrator - Main Coordinator
 * Universal agent for coordinating psychological content creation through multi-agent systems
 *
 * Key Features:
 * - Universal architecture (not tied to specific projects)
 * - Configurable agent workflows
 * - RAG integration support
 * - Modular task delegation
 */

const WorkflowManager = require('./workflow-manager');
const AgentDelegator = require('./agent-delegator');
const RAGConnector = require('../integrations/rag-connector');
const ContentMerger = require('../utils/content-merger');
const QualityValidator = require('../utils/quality-validator');

class PsychologyContentOrchestrator {
    constructor(config = {}) {
        this.config = {
            projectId: config.projectId || null,
            domain: config.domain || 'general-psychology',
            agentConfigs: config.agentConfigs || require('../config/agent-configs'),
            domainSettings: config.domainSettings || require('../config/domain-settings'),
            ragEnabled: config.ragEnabled !== false,
            qualityThreshold: config.qualityThreshold || 0.8,
            maxRetries: config.maxRetries || 3,
            timeout: config.timeout || 300000, // 5 minutes
            ...config
        };

        this.workflowManager = new WorkflowManager(this.config);
        this.agentDelegator = new AgentDelegator(this.config);
        this.ragConnector = this.config.ragEnabled ? new RAGConnector(this.config) : null;
        this.contentMerger = new ContentMerger(this.config);
        this.qualityValidator = new QualityValidator(this.config);

        this.activeWorkflows = new Map();
        this.workflowHistory = [];
        this.metrics = {
            totalRequests: 0,
            successfulCompletions: 0,
            averageCompletionTime: 0,
            qualityScores: []
        };
    }

    /**
     * Main entry point for psychological content creation requests
     * @param {Object} request - Content creation request
     * @param {string} request.type - Type of content (program, assessment, technique, etc.)
     * @param {string} request.description - Detailed description of requirements
     * @param {string} request.domain - Psychological domain (optional, uses config default)
     * @param {Object} request.parameters - Additional parameters specific to content type
     * @param {string} request.targetAudience - Target audience specification
     * @param {Array} request.objectives - Learning/therapeutic objectives
     * @returns {Promise<Object>} Complete psychological content package
     */
    async createContent(request) {
        const startTime = Date.now();
        const workflowId = this.generateWorkflowId();

        try {
            this.metrics.totalRequests++;

            console.log(`[Orchestrator] Starting content creation workflow ${workflowId}`);
            console.log(`[Orchestrator] Request type: ${request.type}, Domain: ${request.domain || this.config.domain}`);

            // Phase 1: Analyze and plan
            const analysisResult = await this.analyzeRequest(request, workflowId);

            // Phase 2: Create workflow plan
            const workflowPlan = await this.workflowManager.createWorkflowPlan(analysisResult, workflowId);

            // Phase 3: Execute multi-agent workflow
            const executionResult = await this.executeWorkflow(workflowPlan, workflowId);

            // Phase 4: Integrate and validate results
            const finalContent = await this.integrateResults(executionResult, workflowId);

            // Phase 5: Quality validation
            const validationResult = await this.validateQuality(finalContent, workflowId);

            if (validationResult.score < this.config.qualityThreshold) {
                console.log(`[Orchestrator] Quality threshold not met (${validationResult.score}), initiating refinement`);
                return await this.refineContent(finalContent, validationResult.feedback, workflowId);
            }

            const completionTime = Date.now() - startTime;
            this.updateMetrics(completionTime, validationResult.score);

            console.log(`[Orchestrator] Workflow ${workflowId} completed successfully in ${completionTime}ms`);

            return {
                success: true,
                workflowId,
                content: finalContent,
                quality: validationResult,
                metrics: {
                    completionTime,
                    agentsUsed: workflowPlan.agents.length,
                    iterationsCount: executionResult.iterations || 1
                },
                metadata: {
                    domain: request.domain || this.config.domain,
                    contentType: request.type,
                    createdAt: new Date().toISOString(),
                    orchestratorVersion: '1.0.0'
                }
            };

        } catch (error) {
            console.error(`[Orchestrator] Workflow ${workflowId} failed:`, error);

            return {
                success: false,
                workflowId,
                error: error.message,
                metrics: {
                    completionTime: Date.now() - startTime,
                    failurePoint: error.phase || 'unknown'
                }
            };
        } finally {
            this.cleanupWorkflow(workflowId);
        }
    }

    /**
     * Analyze incoming request and gather context
     */
    async analyzeRequest(request, workflowId) {
        console.log(`[Orchestrator] Analyzing request for workflow ${workflowId}`);

        const analysis = {
            originalRequest: request,
            domain: request.domain || this.config.domain,
            contentType: request.type,
            complexity: this.assessComplexity(request),
            requiredAgents: [],
            contextData: {},
            ragFindings: null
        };

        // Determine required agents based on content type and complexity
        analysis.requiredAgents = this.determineRequiredAgents(request);

        // Gather domain-specific context via RAG if enabled
        if (this.ragConnector) {
            try {
                analysis.ragFindings = await this.ragConnector.searchRelevantKnowledge(
                    request.description,
                    analysis.domain
                );
                console.log(`[Orchestrator] RAG search found ${analysis.ragFindings.length} relevant documents`);
            } catch (error) {
                console.warn(`[Orchestrator] RAG search failed: ${error.message}`);
            }
        }

        // Add domain-specific analysis
        analysis.domainContext = this.analyzeDomainRequirements(request, analysis.domain);

        this.activeWorkflows.set(workflowId, { analysis, startTime: Date.now() });

        return analysis;
    }

    /**
     * Execute the complete multi-agent workflow
     */
    async executeWorkflow(workflowPlan, workflowId) {
        console.log(`[Orchestrator] Executing workflow ${workflowId} with ${workflowPlan.agents.length} agents`);

        const executionContext = {
            workflowId,
            plan: workflowPlan,
            results: {},
            currentPhase: 0,
            totalPhases: workflowPlan.phases.length
        };

        for (const phase of workflowPlan.phases) {
            console.log(`[Orchestrator] Executing phase ${executionContext.currentPhase + 1}/${executionContext.totalPhases}: ${phase.name}`);

            const phaseResult = await this.executePhase(phase, executionContext);
            executionContext.results[phase.name] = phaseResult;
            executionContext.currentPhase++;

            // Check if phase failed and handle accordingly
            if (!phaseResult.success && phase.critical) {
                throw new Error(`Critical phase '${phase.name}' failed: ${phaseResult.error}`);
            }
        }

        return executionContext.results;
    }

    /**
     * Execute a single phase of the workflow
     */
    async executePhase(phase, executionContext) {
        const phaseStartTime = Date.now();

        try {
            const phaseResults = [];

            // Execute tasks in parallel or sequence based on phase configuration
            if (phase.parallel) {
                const promises = phase.tasks.map(task =>
                    this.agentDelegator.delegateTask(task, executionContext)
                );
                const results = await Promise.allSettled(promises);

                results.forEach((result, index) => {
                    if (result.status === 'fulfilled') {
                        phaseResults.push(result.value);
                    } else {
                        console.error(`[Orchestrator] Task ${phase.tasks[index].name} failed:`, result.reason);
                        phaseResults.push({ success: false, error: result.reason.message });
                    }
                });
            } else {
                // Sequential execution
                for (const task of phase.tasks) {
                    const taskResult = await this.agentDelegator.delegateTask(task, executionContext);
                    phaseResults.push(taskResult);

                    // Update execution context with results for next task
                    executionContext.intermediateResults = phaseResults;
                }
            }

            return {
                success: true,
                phaseName: phase.name,
                results: phaseResults,
                executionTime: Date.now() - phaseStartTime,
                tasksCompleted: phaseResults.filter(r => r.success).length,
                tasksFailed: phaseResults.filter(r => !r.success).length
            };

        } catch (error) {
            return {
                success: false,
                phaseName: phase.name,
                error: error.message,
                executionTime: Date.now() - phaseStartTime
            };
        }
    }

    /**
     * Integrate results from all agents into final content
     */
    async integrateResults(executionResult, workflowId) {
        console.log(`[Orchestrator] Integrating results for workflow ${workflowId}`);

        return await this.contentMerger.mergeResults(executionResult, {
            workflowId,
            domain: this.config.domain,
            integrationStrategy: this.config.domainSettings[this.config.domain]?.integrationStrategy || 'standard'
        });
    }

    /**
     * Validate quality of final content
     */
    async validateQuality(content, workflowId) {
        console.log(`[Orchestrator] Validating quality for workflow ${workflowId}`);

        return await this.qualityValidator.validateContent(content, {
            domain: this.config.domain,
            threshold: this.config.qualityThreshold,
            workflowId
        });
    }

    /**
     * Refine content based on quality feedback
     */
    async refineContent(content, feedback, workflowId) {
        console.log(`[Orchestrator] Refining content for workflow ${workflowId}`);

        // Create refinement workflow
        const refinementRequest = {
            type: 'refinement',
            originalContent: content,
            feedback: feedback,
            targetQuality: this.config.qualityThreshold
        };

        // Execute refinement with subset of agents
        const refinementPlan = await this.workflowManager.createRefinementPlan(refinementRequest, workflowId);
        const refinementResult = await this.executeWorkflow(refinementPlan, `${workflowId}-refinement`);

        return await this.integrateResults(refinementResult, `${workflowId}-refinement`);
    }

    /**
     * Helper methods
     */
    generateWorkflowId() {
        return `wf_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    assessComplexity(request) {
        let complexity = 1;

        if (request.objectives && request.objectives.length > 3) complexity += 1;
        if (request.description && request.description.length > 1000) complexity += 1;
        if (request.parameters && Object.keys(request.parameters).length > 5) complexity += 1;
        if (request.type === 'comprehensive-program') complexity += 2;

        return Math.min(complexity, 5); // Cap at 5
    }

    determineRequiredAgents(request) {
        const baseAgents = ['research', 'architect'];
        const typeSpecificAgents = this.config.agentConfigs.contentTypeMapping[request.type] || [];

        return [...new Set([...baseAgents, ...typeSpecificAgents])];
    }

    analyzeDomainRequirements(request, domain) {
        const domainConfig = this.config.domainSettings[domain] || {};

        return {
            specificRequirements: domainConfig.requirements || [],
            validationCriteria: domainConfig.validation || [],
            recommendedApproaches: domainConfig.approaches || []
        };
    }

    updateMetrics(completionTime, qualityScore) {
        this.metrics.successfulCompletions++;
        this.metrics.qualityScores.push(qualityScore);

        // Update average completion time
        const totalTime = this.metrics.averageCompletionTime * (this.metrics.successfulCompletions - 1) + completionTime;
        this.metrics.averageCompletionTime = totalTime / this.metrics.successfulCompletions;
    }

    cleanupWorkflow(workflowId) {
        if (this.activeWorkflows.has(workflowId)) {
            const workflow = this.activeWorkflows.get(workflowId);
            this.workflowHistory.push({
                ...workflow,
                completedAt: Date.now()
            });
            this.activeWorkflows.delete(workflowId);
        }
    }

    /**
     * Get current orchestrator status and metrics
     */
    getStatus() {
        return {
            activeWorkflows: this.activeWorkflows.size,
            totalProcessed: this.metrics.totalRequests,
            successRate: this.metrics.successfulCompletions / this.metrics.totalRequests,
            averageQuality: this.metrics.qualityScores.reduce((a, b) => a + b, 0) / this.metrics.qualityScores.length,
            averageCompletionTime: this.metrics.averageCompletionTime,
            config: {
                domain: this.config.domain,
                ragEnabled: this.config.ragEnabled,
                qualityThreshold: this.config.qualityThreshold
            }
        };
    }
}

module.exports = PsychologyContentOrchestrator;