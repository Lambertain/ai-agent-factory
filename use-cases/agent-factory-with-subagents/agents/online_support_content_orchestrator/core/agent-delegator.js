/**
 * Agent Delegator - Task delegation and agent coordination
 * Handles the assignment and monitoring of tasks to specialized agents
 */

const EventEmitter = require('events');

class AgentDelegator extends EventEmitter {
    constructor(config) {
        super();
        this.config = config;
        this.agentConfigs = config.agentConfigs;

        // Agent registry and status tracking
        this.availableAgents = new Map();
        this.busyAgents = new Map();
        this.agentMetrics = new Map();
        this.taskQueue = [];
        this.activeTasks = new Map();

        // Load balancing and retry configuration
        this.loadBalancing = {
            strategy: config.loadBalancingStrategy || 'round-robin',
            maxConcurrentTasks: config.maxConcurrentTasks || 5,
            taskTimeout: config.taskTimeout || 300000, // 5 minutes
            retryLimit: config.retryLimit || 3,
            retryDelay: config.retryDelay || 5000 // 5 seconds
        };

        this.initializeAgentRegistry();
    }

    /**
     * Initialize agent registry with available agents
     */
    initializeAgentRegistry() {
        const defaultAgents = [
            'research', 'architect', 'test-generator', 'nlp-generator',
            'technique-designer', 'quality-guardian', 'integrator',
            'domain-expert', 'clinical-expert', 'pedagogy-expert',
            'organizational-expert', 'research-methodologist'
        ];

        defaultAgents.forEach(agentName => {
            this.registerAgent(agentName, {
                type: agentName,
                capabilities: this.getAgentCapabilities(agentName),
                maxConcurrentTasks: this.getAgentConcurrencyLimit(agentName),
                specializations: this.getAgentSpecializations(agentName),
                estimatedResponseTime: this.getAgentResponseTime(agentName)
            });
        });

        console.log(`[AgentDelegator] Initialized registry with ${this.availableAgents.size} agents`);
    }

    /**
     * Register a new agent in the system
     */
    registerAgent(agentName, agentConfig) {
        this.availableAgents.set(agentName, {
            name: agentName,
            config: agentConfig,
            status: 'available',
            currentTasks: 0,
            totalTasksCompleted: 0,
            averageResponseTime: agentConfig.estimatedResponseTime || 60000,
            successRate: 1.0,
            lastUsed: null,
            registeredAt: Date.now()
        });

        this.agentMetrics.set(agentName, {
            tasksAssigned: 0,
            tasksCompleted: 0,
            tasksFailed: 0,
            totalResponseTime: 0,
            averageQualityScore: 0,
            qualityScores: []
        });
    }

    /**
     * Delegate a task to the most appropriate agent
     * @param {Object} task - Task to be delegated
     * @param {Object} executionContext - Current execution context
     * @returns {Promise<Object>} Task execution result
     */
    async delegateTask(task, executionContext) {
        const taskId = this.generateTaskId();
        const startTime = Date.now();

        console.log(`[AgentDelegator] Delegating task ${taskId}: ${task.name || task.type}`);

        try {
            // Find the best agent for this task
            const selectedAgent = await this.selectOptimalAgent(task, executionContext);

            if (!selectedAgent) {
                throw new Error(`No suitable agent found for task: ${task.name || task.type}`);
            }

            // Prepare task context
            const taskContext = this.prepareTaskContext(task, executionContext, taskId);

            // Execute task with selected agent
            const result = await this.executeTaskWithAgent(selectedAgent, taskContext);

            // Update metrics and status
            this.updateAgentMetrics(selectedAgent.name, true, Date.now() - startTime, result.qualityScore);

            console.log(`[AgentDelegator] Task ${taskId} completed successfully by ${selectedAgent.name}`);

            return {
                success: true,
                taskId,
                agentUsed: selectedAgent.name,
                result: result.content,
                metadata: {
                    executionTime: Date.now() - startTime,
                    qualityScore: result.qualityScore,
                    iterations: result.iterations || 1
                }
            };

        } catch (error) {
            console.error(`[AgentDelegator] Task ${taskId} failed:`, error);

            // Try to recover with alternative agent if available
            if (task.retryCount < this.loadBalancing.retryLimit) {
                console.log(`[AgentDelegator] Retrying task ${taskId} (attempt ${task.retryCount + 1})`);

                await this.delay(this.loadBalancing.retryDelay);

                task.retryCount = (task.retryCount || 0) + 1;
                task.excludeAgents = task.excludeAgents || [];
                task.excludeAgents.push(task.lastAttemptedAgent);

                return await this.delegateTask(task, executionContext);
            }

            return {
                success: false,
                taskId,
                error: error.message,
                metadata: {
                    executionTime: Date.now() - startTime,
                    retryCount: task.retryCount || 0,
                    lastAttemptedAgent: task.lastAttemptedAgent
                }
            };
        }
    }

    /**
     * Select the optimal agent for a given task
     */
    async selectOptimalAgent(task, executionContext) {
        const candidateAgents = this.findCandidateAgents(task);

        if (candidateAgents.length === 0) {
            return null;
        }

        // Apply selection strategy
        switch (this.loadBalancing.strategy) {
            case 'round-robin':
                return this.selectRoundRobin(candidateAgents);

            case 'least-loaded':
                return this.selectLeastLoaded(candidateAgents);

            case 'best-performance':
                return this.selectBestPerformance(candidateAgents, task);

            case 'specialized':
                return this.selectMostSpecialized(candidateAgents, task);

            default:
                return this.selectBestFit(candidateAgents, task, executionContext);
        }
    }

    /**
     * Find candidate agents that can handle the task
     */
    findCandidateAgents(task) {
        const requiredCapabilities = this.getTaskRequiredCapabilities(task);
        const excludedAgents = task.excludeAgents || [];

        const candidates = [];

        this.availableAgents.forEach((agent, agentName) => {
            // Skip excluded agents
            if (excludedAgents.includes(agentName)) {
                return;
            }

            // Check if agent is available
            if (agent.status !== 'available' && agent.currentTasks >= agent.config.maxConcurrentTasks) {
                return;
            }

            // Check capability match
            const hasRequiredCapabilities = requiredCapabilities.every(capability =>
                agent.config.capabilities.includes(capability)
            );

            if (hasRequiredCapabilities) {
                candidates.push(agent);
            }
        });

        return candidates;
    }

    /**
     * Agent selection strategies
     */
    selectRoundRobin(candidates) {
        // Select agent that was used least recently
        return candidates.reduce((best, current) => {
            const bestLastUsed = best.lastUsed || 0;
            const currentLastUsed = current.lastUsed || 0;

            return currentLastUsed < bestLastUsed ? current : best;
        });
    }

    selectLeastLoaded(candidates) {
        return candidates.reduce((best, current) => {
            return current.currentTasks < best.currentTasks ? current : best;
        });
    }

    selectBestPerformance(candidates, task) {
        return candidates.reduce((best, current) => {
            const bestScore = this.calculatePerformanceScore(best, task);
            const currentScore = this.calculatePerformanceScore(current, task);

            return currentScore > bestScore ? current : best;
        });
    }

    selectMostSpecialized(candidates, task) {
        const taskDomain = this.getTaskDomain(task);

        return candidates.reduce((best, current) => {
            const bestSpecialization = this.getSpecializationMatch(best, taskDomain);
            const currentSpecialization = this.getSpecializationMatch(current, taskDomain);

            return currentSpecialization > bestSpecialization ? current : best;
        });
    }

    selectBestFit(candidates, task, executionContext) {
        // Comprehensive scoring considering multiple factors
        return candidates.reduce((best, current) => {
            const bestScore = this.calculateOverallFitScore(best, task, executionContext);
            const currentScore = this.calculateOverallFitScore(current, task, executionContext);

            return currentScore > bestScore ? current : best;
        });
    }

    /**
     * Execute task with selected agent
     */
    async executeTaskWithAgent(agent, taskContext) {
        const agentName = agent.name;
        const taskId = taskContext.taskId;

        // Update agent status
        this.updateAgentStatus(agentName, 'busy');
        this.activeTasks.set(taskId, { agent: agentName, startTime: Date.now() });

        try {
            // Simulate agent execution (in real implementation, this would call actual agents)
            const result = await this.simulateAgentExecution(agent, taskContext);

            // Validate result quality
            const qualityScore = await this.validateTaskResult(result, taskContext);

            return {
                content: result,
                qualityScore,
                iterations: 1,
                agentUsed: agentName
            };

        } finally {
            // Update agent status
            this.updateAgentStatus(agentName, 'available');
            this.activeTasks.delete(taskId);
        }
    }

    /**
     * Simulate agent execution (placeholder for actual agent integration)
     */
    async simulateAgentExecution(agent, taskContext) {
        const agentType = agent.config.type;
        const task = taskContext.task;

        // Simulate processing time based on agent type and task complexity
        const processingTime = this.calculateProcessingTime(agent, task);
        await this.delay(Math.min(processingTime, 1000)); // Cap simulation delay

        // Generate result based on agent type and task
        return this.generateMockResult(agentType, task, taskContext);
    }

    /**
     * Generate mock result for simulation
     */
    generateMockResult(agentType, task, taskContext) {
        const baseResult = {
            taskId: taskContext.taskId,
            agentType,
            completedAt: new Date().toISOString(),
            workflowId: taskContext.workflowId
        };

        switch (agentType) {
            case 'research':
                return {
                    ...baseResult,
                    evidenceBase: ['evidence1', 'evidence2', 'evidence3'],
                    recommendations: ['rec1', 'rec2'],
                    qualityIndicators: { reliability: 0.9, validity: 0.85 }
                };

            case 'architect':
                return {
                    ...baseResult,
                    structure: { modules: [], dependencies: [] },
                    framework: 'cognitive-behavioral',
                    designPrinciples: ['modularity', 'scalability']
                };

            case 'test-generator':
                return {
                    ...baseResult,
                    assessments: [{ type: 'pre-test', questions: 10 }],
                    validationCriteria: { reliability: 0.8, validity: 0.75 }
                };

            case 'nlp-generator':
                return {
                    ...baseResult,
                    techniques: ['technique1', 'technique2'],
                    exercises: ['exercise1', 'exercise2'],
                    adaptations: { beginner: 'adaptation1', advanced: 'adaptation2' }
                };

            case 'quality-guardian':
                return {
                    ...baseResult,
                    qualityScore: 0.85,
                    validationResults: { passed: true, issues: [] },
                    recommendations: ['improve clarity', 'add examples']
                };

            default:
                return {
                    ...baseResult,
                    output: `Generated content from ${agentType}`,
                    metadata: { contentType: task.type, domain: taskContext.domain }
                };
        }
    }

    /**
     * Validate task result quality
     */
    async validateTaskResult(result, taskContext) {
        // Basic quality validation
        let qualityScore = 0.5;

        // Check completeness
        if (result && typeof result === 'object' && Object.keys(result).length > 3) {
            qualityScore += 0.2;
        }

        // Check for quality indicators in result
        if (result.qualityIndicators || result.qualityScore) {
            qualityScore += 0.2;
        }

        // Check domain alignment
        if (result.metadata && result.metadata.domain === taskContext.domain) {
            qualityScore += 0.1;
        }

        return Math.min(qualityScore, 1.0);
    }

    /**
     * Helper methods for agent selection
     */
    calculatePerformanceScore(agent, task) {
        const metrics = this.agentMetrics.get(agent.name);
        if (!metrics) return 0;

        const successRate = metrics.tasksCompleted / (metrics.tasksAssigned || 1);
        const averageQuality = metrics.averageQualityScore || 0.5;
        const responseTimeScore = 1 - (agent.averageResponseTime / 300000); // Normalize to 5 minutes

        return (successRate * 0.4 + averageQuality * 0.4 + Math.max(responseTimeScore, 0) * 0.2);
    }

    calculateOverallFitScore(agent, task, executionContext) {
        const performanceScore = this.calculatePerformanceScore(agent, task);
        const specializationScore = this.getSpecializationMatch(agent, this.getTaskDomain(task));
        const loadScore = 1 - (agent.currentTasks / agent.config.maxConcurrentTasks);

        return (performanceScore * 0.5 + specializationScore * 0.3 + loadScore * 0.2);
    }

    getSpecializationMatch(agent, taskDomain) {
        if (!agent.config.specializations) return 0.5;

        const specializations = agent.config.specializations;
        if (specializations.includes(taskDomain)) return 1.0;
        if (specializations.includes('general')) return 0.7;

        return 0.3;
    }

    /**
     * Utility methods
     */
    prepareTaskContext(task, executionContext, taskId) {
        return {
            taskId,
            task,
            workflowId: executionContext.workflowId,
            domain: executionContext.plan?.domain || this.config.domain,
            previousResults: executionContext.intermediateResults || [],
            ragData: executionContext.ragData,
            requirements: task.requirements || [],
            constraints: task.constraints || []
        };
    }

    getTaskRequiredCapabilities(task) {
        const capabilityMap = {
            'research': ['research', 'analysis', 'evidence-synthesis'],
            'architecture': ['design', 'planning', 'systems-thinking'],
            'assessment': ['psychometrics', 'testing', 'validation'],
            'content-generation': ['content-creation', 'writing', 'adaptation'],
            'quality-validation': ['quality-assurance', 'review', 'validation'],
            'integration': ['synthesis', 'integration', 'coordination']
        };

        return capabilityMap[task.type] || capabilityMap[task.name] || ['general'];
    }

    getTaskDomain(task) {
        return task.domain || this.config.domain || 'general-psychology';
    }

    calculateProcessingTime(agent, task) {
        const baseTime = 30000; // 30 seconds
        const complexityMultiplier = (task.complexity || 1) * 1.2;
        const agentMultiplier = agent.config.estimatedResponseTime / 60000; // Normalize to minutes

        return baseTime * complexityMultiplier * agentMultiplier;
    }

    updateAgentStatus(agentName, status) {
        const agent = this.availableAgents.get(agentName);
        if (agent) {
            agent.status = status;
            agent.lastUsed = Date.now();

            if (status === 'busy') {
                agent.currentTasks++;
            } else if (status === 'available' && agent.currentTasks > 0) {
                agent.currentTasks--;
            }
        }
    }

    updateAgentMetrics(agentName, success, responseTime, qualityScore = null) {
        const metrics = this.agentMetrics.get(agentName);
        const agent = this.availableAgents.get(agentName);

        if (metrics && agent) {
            metrics.tasksAssigned++;

            if (success) {
                metrics.tasksCompleted++;
                agent.totalTasksCompleted++;

                // Update average response time
                metrics.totalResponseTime += responseTime;
                agent.averageResponseTime = metrics.totalResponseTime / metrics.tasksCompleted;

                // Update quality score
                if (qualityScore !== null) {
                    metrics.qualityScores.push(qualityScore);
                    metrics.averageQualityScore = metrics.qualityScores.reduce((a, b) => a + b, 0) / metrics.qualityScores.length;
                }
            } else {
                metrics.tasksFailed++;
            }

            // Update success rate
            agent.successRate = metrics.tasksCompleted / metrics.tasksAssigned;
        }
    }

    generateTaskId() {
        return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Agent configuration methods
     */
    getAgentCapabilities(agentName) {
        const capabilityMap = {
            'research': ['research', 'analysis', 'evidence-synthesis', 'literature-review'],
            'architect': ['design', 'planning', 'systems-thinking', 'framework-design'],
            'test-generator': ['psychometrics', 'testing', 'validation', 'assessment-design'],
            'nlp-generator': ['content-creation', 'writing', 'language-processing', 'adaptation'],
            'technique-designer': ['technique-development', 'intervention-design', 'creativity'],
            'quality-guardian': ['quality-assurance', 'review', 'validation', 'standards-compliance'],
            'integrator': ['synthesis', 'integration', 'coordination', 'content-merging'],
            'domain-expert': ['domain-knowledge', 'specialization', 'expert-review'],
            'clinical-expert': ['clinical-psychology', 'therapeutic-approaches', 'evidence-based-practice'],
            'pedagogy-expert': ['educational-psychology', 'learning-theory', 'curriculum-design']
        };

        return capabilityMap[agentName] || ['general'];
    }

    getAgentConcurrencyLimit(agentName) {
        const limits = {
            'research': 3,
            'architect': 2,
            'test-generator': 2,
            'nlp-generator': 4,
            'technique-designer': 3,
            'quality-guardian': 5,
            'integrator': 1,
            'domain-expert': 2
        };

        return limits[agentName] || 2;
    }

    getAgentSpecializations(agentName) {
        const specializations = {
            'clinical-expert': ['clinical-psychology', 'therapy', 'mental-health'],
            'pedagogy-expert': ['educational-psychology', 'learning', 'teaching'],
            'organizational-expert': ['organizational-psychology', 'workplace', 'leadership'],
            'research-methodologist': ['research-methods', 'statistics', 'experimental-design']
        };

        return specializations[agentName] || ['general'];
    }

    getAgentResponseTime(agentName) {
        const responseTimes = {
            'research': 120000, // 2 minutes
            'architect': 180000, // 3 minutes
            'test-generator': 150000, // 2.5 minutes
            'nlp-generator': 90000, // 1.5 minutes
            'quality-guardian': 60000, // 1 minute
            'integrator': 240000 // 4 minutes
        };

        return responseTimes[agentName] || 120000;
    }

    /**
     * Get current delegation status and metrics
     */
    getStatus() {
        const activeAgents = Array.from(this.availableAgents.values()).filter(a => a.status === 'busy').length;
        const totalTasks = Array.from(this.agentMetrics.values()).reduce((sum, m) => sum + m.tasksAssigned, 0);
        const completedTasks = Array.from(this.agentMetrics.values()).reduce((sum, m) => sum + m.tasksCompleted, 0);

        return {
            availableAgents: this.availableAgents.size,
            activeAgents,
            activeTasks: this.activeTasks.size,
            queuedTasks: this.taskQueue.length,
            totalTasksProcessed: totalTasks,
            successRate: totalTasks > 0 ? completedTasks / totalTasks : 0,
            agentMetrics: Object.fromEntries(this.agentMetrics),
            loadBalancingStrategy: this.loadBalancing.strategy
        };
    }
}

module.exports = AgentDelegator;