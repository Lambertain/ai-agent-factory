/**
 * Workflow Manager - Dynamic workflow planning and execution management
 * Handles the creation and management of multi-agent workflows for psychological content creation
 */

class WorkflowManager {
    constructor(config) {
        this.config = config;
        this.agentConfigs = config.agentConfigs;
        this.domainSettings = config.domainSettings;

        // Default workflow templates for different content types
        this.workflowTemplates = {
            'therapeutic-program': {
                phases: [
                    { name: 'research', agents: ['research'], parallel: false, critical: true },
                    { name: 'assessment', agents: ['test-generator'], parallel: false, critical: true },
                    { name: 'architecture', agents: ['architect'], parallel: false, critical: true },
                    { name: 'content-generation', agents: ['nlp-generator', 'technique-designer'], parallel: true, critical: true },
                    { name: 'integration', agents: ['integrator'], parallel: false, critical: true },
                    { name: 'validation', agents: ['quality-guardian'], parallel: false, critical: true }
                ],
                estimatedDuration: 1800000, // 30 minutes
                complexity: 'high'
            },
            'assessment-tool': {
                phases: [
                    { name: 'research', agents: ['research'], parallel: false, critical: true },
                    { name: 'psychometric-design', agents: ['test-generator', 'psychometrician'], parallel: true, critical: true },
                    { name: 'validation-design', agents: ['quality-guardian'], parallel: false, critical: true },
                    { name: 'implementation', agents: ['nlp-generator'], parallel: false, critical: false }
                ],
                estimatedDuration: 1200000, // 20 minutes
                complexity: 'medium'
            },
            'technique-library': {
                phases: [
                    { name: 'research', agents: ['research'], parallel: false, critical: true },
                    { name: 'technique-development', agents: ['nlp-generator', 'technique-designer'], parallel: true, critical: true },
                    { name: 'categorization', agents: ['architect'], parallel: false, critical: false },
                    { name: 'validation', agents: ['quality-guardian'], parallel: false, critical: true }
                ],
                estimatedDuration: 900000, // 15 minutes
                complexity: 'medium'
            },
            'comprehensive-program': {
                phases: [
                    { name: 'strategic-research', agents: ['research', 'domain-expert'], parallel: true, critical: true },
                    { name: 'needs-assessment', agents: ['test-generator'], parallel: false, critical: true },
                    { name: 'program-architecture', agents: ['architect', 'curriculum-designer'], parallel: true, critical: true },
                    { name: 'content-creation', agents: ['nlp-generator', 'technique-designer', 'assessment-creator'], parallel: true, critical: true },
                    { name: 'integration-synthesis', agents: ['integrator'], parallel: false, critical: true },
                    { name: 'quality-assurance', agents: ['quality-guardian', 'peer-reviewer'], parallel: true, critical: true },
                    { name: 'pilot-preparation', agents: ['implementation-specialist'], parallel: false, critical: false }
                ],
                estimatedDuration: 3600000, // 60 minutes
                complexity: 'very-high'
            },
            'refinement': {
                phases: [
                    { name: 'feedback-analysis', agents: ['quality-guardian'], parallel: false, critical: true },
                    { name: 'targeted-improvement', agents: ['nlp-generator'], parallel: false, critical: true },
                    { name: 'revalidation', agents: ['quality-guardian'], parallel: false, critical: true }
                ],
                estimatedDuration: 600000, // 10 minutes
                complexity: 'low'
            }
        };

        // Dynamic workflow rules
        this.workflowRules = {
            complexity: {
                1: { maxAgents: 3, maxPhases: 4, timeMultiplier: 1.0 },
                2: { maxAgents: 5, maxPhases: 6, timeMultiplier: 1.2 },
                3: { maxAgents: 7, maxPhases: 8, timeMultiplier: 1.5 },
                4: { maxAgents: 10, maxPhases: 10, timeMultiplier: 2.0 },
                5: { maxAgents: 12, maxPhases: 12, timeMultiplier: 2.5 }
            },
            domain: {
                'clinical-psychology': {
                    requiredAgents: ['clinical-expert', 'ethics-reviewer'],
                    additionalPhases: ['ethical-review', 'clinical-validation']
                },
                'educational-psychology': {
                    requiredAgents: ['pedagogy-expert', 'curriculum-designer'],
                    additionalPhases: ['educational-alignment', 'learning-outcome-validation']
                },
                'organizational-psychology': {
                    requiredAgents: ['organizational-expert', 'change-management'],
                    additionalPhases: ['stakeholder-analysis', 'implementation-planning']
                },
                'research-psychology': {
                    requiredAgents: ['research-methodologist', 'statistical-analyst'],
                    additionalPhases: ['methodology-design', 'statistical-planning']
                }
            }
        };
    }

    /**
     * Create a comprehensive workflow plan based on analysis results
     * @param {Object} analysisResult - Results from request analysis
     * @param {string} workflowId - Unique workflow identifier
     * @returns {Object} Complete workflow plan
     */
    async createWorkflowPlan(analysisResult, workflowId) {
        console.log(`[WorkflowManager] Creating workflow plan for ${workflowId}`);

        const contentType = analysisResult.contentType;
        const complexity = analysisResult.complexity;
        const domain = analysisResult.domain;

        // Start with base template
        let workflow = this.getBaseWorkflowTemplate(contentType);

        // Apply complexity adjustments
        workflow = this.applyComplexityRules(workflow, complexity);

        // Apply domain-specific modifications
        workflow = this.applyDomainRules(workflow, domain);

        // Add dynamic phases based on analysis
        workflow = this.addDynamicPhases(workflow, analysisResult);

        // Optimize agent allocation
        workflow = this.optimizeAgentAllocation(workflow, analysisResult);

        // Add RAG integration points
        if (this.config.ragEnabled && analysisResult.ragFindings) {
            workflow = this.addRAGIntegrationPoints(workflow, analysisResult.ragFindings);
        }

        // Calculate dependencies and timing
        workflow = this.calculateWorkflowTiming(workflow);

        // Add quality checkpoints
        workflow = this.addQualityCheckpoints(workflow);

        const finalPlan = {
            workflowId,
            contentType,
            domain,
            complexity,
            workflow,
            metadata: {
                createdAt: new Date().toISOString(),
                estimatedDuration: workflow.estimatedDuration,
                totalAgents: this.countUniqueAgents(workflow),
                totalPhases: workflow.phases.length,
                criticalPhases: workflow.phases.filter(p => p.critical).length
            }
        };

        console.log(`[WorkflowManager] Created workflow plan with ${finalPlan.metadata.totalPhases} phases and ${finalPlan.metadata.totalAgents} agents`);

        return finalPlan;
    }

    /**
     * Create a refinement workflow plan
     */
    async createRefinementPlan(refinementRequest, workflowId) {
        console.log(`[WorkflowManager] Creating refinement plan for ${workflowId}`);

        const baseWorkflow = this.workflowTemplates['refinement'];

        // Customize based on feedback type
        const customizedWorkflow = this.customizeRefinementWorkflow(baseWorkflow, refinementRequest.feedback);

        return {
            workflowId: `${workflowId}-refinement`,
            contentType: 'refinement',
            workflow: customizedWorkflow,
            originalContent: refinementRequest.originalContent,
            feedback: refinementRequest.feedback,
            metadata: {
                createdAt: new Date().toISOString(),
                estimatedDuration: customizedWorkflow.estimatedDuration,
                refinementType: this.classifyRefinementType(refinementRequest.feedback)
            }
        };
    }

    /**
     * Get base workflow template for content type
     */
    getBaseWorkflowTemplate(contentType) {
        const template = this.workflowTemplates[contentType] || this.workflowTemplates['therapeutic-program'];
        return JSON.parse(JSON.stringify(template)); // Deep clone
    }

    /**
     * Apply complexity-based modifications to workflow
     */
    applyComplexityRules(workflow, complexity) {
        const rules = this.workflowRules.complexity[complexity] || this.workflowRules.complexity[3];

        // Adjust timing based on complexity
        workflow.estimatedDuration = Math.floor(workflow.estimatedDuration * rules.timeMultiplier);

        // Add additional phases for high complexity
        if (complexity >= 4) {
            workflow.phases.push({
                name: 'peer-review',
                agents: ['peer-reviewer', 'domain-expert'],
                parallel: true,
                critical: false
            });
        }

        if (complexity === 5) {
            workflow.phases.push({
                name: 'expert-consultation',
                agents: ['senior-expert', 'methodology-expert'],
                parallel: false,
                critical: true
            });
        }

        return workflow;
    }

    /**
     * Apply domain-specific rules and requirements
     */
    applyDomainRules(workflow, domain) {
        const domainRules = this.workflowRules.domain[domain];

        if (domainRules) {
            // Add required agents to existing phases
            workflow.phases.forEach(phase => {
                domainRules.requiredAgents?.forEach(agent => {
                    if (!phase.agents.includes(agent)) {
                        phase.agents.push(agent);
                    }
                });
            });

            // Add domain-specific phases
            domainRules.additionalPhases?.forEach(phaseName => {
                if (!workflow.phases.find(p => p.name === phaseName)) {
                    workflow.phases.push({
                        name: phaseName,
                        agents: domainRules.requiredAgents || ['domain-expert'],
                        parallel: false,
                        critical: true
                    });
                }
            });
        }

        return workflow;
    }

    /**
     * Add dynamic phases based on specific analysis results
     */
    addDynamicPhases(workflow, analysisResult) {
        // Add phases based on specific requirements
        if (analysisResult.originalRequest.targetAudience) {
            const audiencePhase = {
                name: 'audience-adaptation',
                agents: ['audience-specialist', 'adaptation-expert'],
                parallel: false,
                critical: false
            };

            // Insert before final validation
            const validationIndex = workflow.phases.findIndex(p => p.name === 'validation');
            if (validationIndex > -1) {
                workflow.phases.splice(validationIndex, 0, audiencePhase);
            } else {
                workflow.phases.push(audiencePhase);
            }
        }

        // Add cultural adaptation if needed
        if (analysisResult.domainContext.specificRequirements?.includes('cultural-sensitivity')) {
            workflow.phases.push({
                name: 'cultural-adaptation',
                agents: ['cultural-expert', 'adaptation-specialist'],
                parallel: false,
                critical: true
            });
        }

        // Add accessibility phase if required
        if (analysisResult.originalRequest.parameters?.accessibility) {
            workflow.phases.push({
                name: 'accessibility-optimization',
                agents: ['accessibility-expert', 'inclusive-design'],
                parallel: false,
                critical: false
            });
        }

        return workflow;
    }

    /**
     * Optimize agent allocation across phases
     */
    optimizeAgentAllocation(workflow, analysisResult) {
        // Remove duplicate agents and optimize load distribution
        workflow.phases.forEach(phase => {
            phase.agents = [...new Set(phase.agents)]; // Remove duplicates

            // Ensure minimum agent count for parallel phases
            if (phase.parallel && phase.agents.length < 2) {
                phase.parallel = false;
            }

            // Add load balancing for heavy phases
            if (phase.agents.length > 4) {
                phase.loadBalanced = true;
                phase.batchSize = 2;
            }
        });

        return workflow;
    }

    /**
     * Add RAG integration points to workflow
     */
    addRAGIntegrationPoints(workflow, ragFindings) {
        workflow.phases.forEach(phase => {
            if (['research', 'architecture', 'content-generation'].includes(phase.name)) {
                phase.ragIntegration = {
                    enabled: true,
                    relevantDocuments: ragFindings.filter(doc =>
                        doc.relevance > 0.7 && doc.categories?.includes(phase.name)
                    ).slice(0, 5), // Top 5 relevant documents per phase
                    searchQueries: this.generateRAGQueries(phase.name, ragFindings)
                };
            }
        });

        return workflow;
    }

    /**
     * Calculate workflow timing and dependencies
     */
    calculateWorkflowTiming(workflow) {
        let totalTime = 0;
        let currentTime = 0;

        workflow.phases.forEach((phase, index) => {
            const phaseTime = this.estimatePhaseTime(phase);

            phase.timing = {
                estimatedDuration: phaseTime,
                startTime: currentTime,
                endTime: currentTime + phaseTime,
                dependencies: index > 0 ? [workflow.phases[index - 1].name] : []
            };

            if (phase.parallel && index > 0) {
                // Parallel phases can start at the same time as the previous phase
                phase.timing.startTime = workflow.phases[index - 1].timing.startTime;
                phase.timing.endTime = phase.timing.startTime + phaseTime;
                totalTime = Math.max(totalTime, phase.timing.endTime);
            } else {
                currentTime += phaseTime;
                totalTime = currentTime;
            }
        });

        workflow.estimatedDuration = totalTime;
        return workflow;
    }

    /**
     * Add quality checkpoints throughout workflow
     */
    addQualityCheckpoints(workflow) {
        const checkpointInterval = Math.ceil(workflow.phases.length / 3);

        for (let i = checkpointInterval; i < workflow.phases.length; i += checkpointInterval) {
            const checkpoint = {
                name: `quality-checkpoint-${Math.floor(i / checkpointInterval)}`,
                agents: ['quality-guardian'],
                parallel: false,
                critical: false,
                isCheckpoint: true,
                checkpointCriteria: this.getCheckpointCriteria(workflow.phases.slice(i - checkpointInterval, i))
            };

            workflow.phases.splice(i, 0, checkpoint);
        }

        return workflow;
    }

    /**
     * Helper methods
     */
    estimatePhaseTime(phase) {
        const baseTime = 180000; // 3 minutes per agent
        const agentTime = phase.agents.length * baseTime;
        const complexityMultiplier = phase.critical ? 1.5 : 1.0;
        const parallelDivider = phase.parallel ? 1.5 : 1.0;

        return Math.floor((agentTime * complexityMultiplier) / parallelDivider);
    }

    countUniqueAgents(workflow) {
        const allAgents = workflow.phases.flatMap(phase => phase.agents);
        return new Set(allAgents).size;
    }

    generateRAGQueries(phaseName, ragFindings) {
        const queryMap = {
            'research': ['methodology', 'evidence-base', 'best-practices'],
            'architecture': ['framework', 'structure', 'design-patterns'],
            'content-generation': ['templates', 'examples', 'techniques']
        };

        return queryMap[phaseName] || ['general-knowledge'];
    }

    customizeRefinementWorkflow(baseWorkflow, feedback) {
        const refinementType = this.classifyRefinementType(feedback);

        const customWorkflow = JSON.parse(JSON.stringify(baseWorkflow));

        switch (refinementType) {
            case 'content-quality':
                customWorkflow.phases[1].agents.push('content-editor');
                break;
            case 'scientific-accuracy':
                customWorkflow.phases[1].agents.push('research-validator', 'fact-checker');
                break;
            case 'user-experience':
                customWorkflow.phases[1].agents.push('ux-specialist', 'accessibility-expert');
                break;
            case 'comprehensive':
                customWorkflow.phases[1].agents.push('content-editor', 'research-validator', 'ux-specialist');
                customWorkflow.estimatedDuration *= 1.5;
                break;
        }

        return customWorkflow;
    }

    classifyRefinementType(feedback) {
        const feedbackText = JSON.stringify(feedback).toLowerCase();

        if (feedbackText.includes('content') || feedbackText.includes('clarity')) return 'content-quality';
        if (feedbackText.includes('research') || feedbackText.includes('evidence')) return 'scientific-accuracy';
        if (feedbackText.includes('user') || feedbackText.includes('experience')) return 'user-experience';

        return 'comprehensive';
    }

    getCheckpointCriteria(phases) {
        return {
            completionRate: 1.0,
            qualityThreshold: 0.7,
            phasesEvaluated: phases.map(p => p.name),
            evaluationAspects: ['completeness', 'quality', 'alignment']
        };
    }

    /**
     * Get workflow statistics and insights
     */
    getWorkflowInsights(workflow) {
        return {
            complexity: workflow.complexity,
            totalPhases: workflow.phases.length,
            parallelPhases: workflow.phases.filter(p => p.parallel).length,
            criticalPhases: workflow.phases.filter(p => p.critical).length,
            uniqueAgents: this.countUniqueAgents(workflow),
            estimatedDuration: workflow.estimatedDuration,
            qualityCheckpoints: workflow.phases.filter(p => p.isCheckpoint).length,
            ragIntegration: workflow.phases.filter(p => p.ragIntegration?.enabled).length
        };
    }
}

module.exports = WorkflowManager;