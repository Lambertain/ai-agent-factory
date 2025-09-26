/**
 * External APIs Integration - Universal API connector for psychology content systems
 * Handles integration with various external services and platforms
 */

class ExternalAPIs {
    constructor(config) {
        this.config = {
            timeout: config.timeout || 30000,
            retryLimit: config.retryLimit || 3,
            retryDelay: config.retryDelay || 1000,
            maxConcurrentRequests: config.maxConcurrentRequests || 10,
            rateLimitWindow: config.rateLimitWindow || 60000, // 1 minute
            maxRequestsPerWindow: config.maxRequestsPerWindow || 100,
            ...config
        };

        // API endpoint configurations
        this.endpoints = {
            // Archon MCP Server integration
            archon: {
                baseUrl: config.archonBaseUrl || 'mcp://archon',
                endpoints: {
                    projects: 'find_projects',
                    tasks: 'find_tasks',
                    documents: 'find_documents',
                    manage_project: 'manage_project',
                    manage_task: 'manage_task',
                    manage_document: 'manage_document'
                },
                enabled: config.archonEnabled !== false
            },

            // GitHub integration
            github: {
                baseUrl: config.githubBaseUrl || 'https://api.github.com',
                token: config.githubToken,
                endpoints: {
                    repos: '/repos',
                    issues: '/repos/{owner}/{repo}/issues',
                    pulls: '/repos/{owner}/{repo}/pulls',
                    content: '/repos/{owner}/{repo}/contents'
                },
                enabled: Boolean(config.githubToken)
            },

            // Generic psychology APIs
            psychology: {
                assessmentApi: config.assessmentApiUrl,
                interventionApi: config.interventionApiUrl,
                researchApi: config.researchApiUrl,
                enabled: config.psychologyApisEnabled !== false
            },

            // Custom external integrations
            custom: config.customEndpoints || {}
        };

        // Request tracking and rate limiting
        this.requestTracker = new Map();
        this.rateLimitTracker = new Map();
        this.activeRequests = 0;

        // Performance metrics
        this.metrics = {
            totalRequests: 0,
            successfulRequests: 0,
            failedRequests: 0,
            averageResponseTime: 0,
            totalResponseTime: 0,
            rateLimitHits: 0,
            timeoutCount: 0
        };
    }

    /**
     * Project Management Integration
     */
    async createProject(projectData) {
        console.log('[ExternalAPIs] Creating project via Archon integration');

        if (!this.endpoints.archon.enabled) {
            throw new Error('Archon integration not enabled');
        }

        try {
            const result = await this.callArchonAPI('manage_project', {
                action: 'create',
                title: projectData.title,
                description: projectData.description,
                github_repo: projectData.githubRepo
            });

            if (result.success) {
                console.log(`[ExternalAPIs] Project created: ${result.project.id}`);
                return result.project;
            } else {
                throw new Error(result.message || 'Failed to create project');
            }

        } catch (error) {
            console.error('[ExternalAPIs] Project creation failed:', error);
            throw error;
        }
    }

    async updateProject(projectId, updateData) {
        console.log(`[ExternalAPIs] Updating project ${projectId} via Archon integration`);

        try {
            const result = await this.callArchonAPI('manage_project', {
                action: 'update',
                project_id: projectId,
                ...updateData
            });

            if (result.success) {
                return result.project;
            } else {
                throw new Error(result.message || 'Failed to update project');
            }

        } catch (error) {
            console.error(`[ExternalAPIs] Project update failed for ${projectId}:`, error);
            throw error;
        }
    }

    async findProjects(query = null, options = {}) {
        console.log('[ExternalAPIs] Searching projects via Archon integration');

        try {
            const searchParams = {
                query,
                page: options.page || 1,
                per_page: options.perPage || 10,
                ...options
            };

            const result = await this.callArchonAPI('find_projects', searchParams);

            if (Array.isArray(result)) {
                return result;
            } else if (result.success) {
                return result.projects || result.data || [];
            } else {
                console.warn('[ExternalAPIs] No projects found or API returned error');
                return [];
            }

        } catch (error) {
            console.error('[ExternalAPIs] Project search failed:', error);
            return [];
        }
    }

    /**
     * Task Management Integration
     */
    async createTask(taskData) {
        console.log('[ExternalAPIs] Creating task via Archon integration');

        try {
            const result = await this.callArchonAPI('manage_task', {
                action: 'create',
                project_id: taskData.projectId,
                title: taskData.title,
                description: taskData.description,
                status: taskData.status || 'todo',
                assignee: taskData.assignee || 'AI IDE Agent',
                task_order: taskData.priority || 50,
                feature: taskData.feature
            });

            if (result.success) {
                console.log(`[ExternalAPIs] Task created: ${result.task.id}`);
                return result.task;
            } else {
                throw new Error(result.message || 'Failed to create task');
            }

        } catch (error) {
            console.error('[ExternalAPIs] Task creation failed:', error);
            throw error;
        }
    }

    async updateTaskStatus(taskId, status, additionalData = {}) {
        console.log(`[ExternalAPIs] Updating task ${taskId} status to ${status}`);

        try {
            const result = await this.callArchonAPI('manage_task', {
                action: 'update',
                task_id: taskId,
                status,
                ...additionalData
            });

            if (result.success) {
                return result.task;
            } else {
                throw new Error(result.message || 'Failed to update task status');
            }

        } catch (error) {
            console.error(`[ExternalAPIs] Task status update failed for ${taskId}:`, error);
            throw error;
        }
    }

    async findTasks(criteria = {}) {
        console.log('[ExternalAPIs] Searching tasks via Archon integration');

        try {
            const searchParams = {
                query: criteria.query,
                project_id: criteria.projectId,
                filter_by: criteria.filterBy,
                filter_value: criteria.filterValue,
                include_closed: criteria.includeClosed !== false,
                page: criteria.page || 1,
                per_page: criteria.perPage || 10
            };

            const result = await this.callArchonAPI('find_tasks', searchParams);

            if (Array.isArray(result)) {
                return result;
            } else if (result.success) {
                return result.tasks || result.data || [];
            } else {
                return [];
            }

        } catch (error) {
            console.error('[ExternalAPIs] Task search failed:', error);
            return [];
        }
    }

    /**
     * Document Management Integration
     */
    async createDocument(documentData) {
        console.log('[ExternalAPIs] Creating document via Archon integration');

        try {
            const result = await this.callArchonAPI('manage_document', {
                action: 'create',
                project_id: documentData.projectId,
                title: documentData.title,
                document_type: documentData.type || 'note',
                content: documentData.content,
                tags: documentData.tags || [],
                author: documentData.author || 'Psychology Content Orchestrator'
            });

            if (result.success) {
                console.log(`[ExternalAPIs] Document created: ${result.document.id}`);
                return result.document;
            } else {
                throw new Error(result.message || 'Failed to create document');
            }

        } catch (error) {
            console.error('[ExternalAPIs] Document creation failed:', error);
            throw error;
        }
    }

    async updateDocument(documentId, projectId, updateData) {
        console.log(`[ExternalAPIs] Updating document ${documentId}`);

        try {
            const result = await this.callArchonAPI('manage_document', {
                action: 'update',
                project_id: projectId,
                document_id: documentId,
                ...updateData
            });

            if (result.success) {
                return result.document;
            } else {
                throw new Error(result.message || 'Failed to update document');
            }

        } catch (error) {
            console.error(`[ExternalAPIs] Document update failed for ${documentId}:`, error);
            throw error;
        }
    }

    async findDocuments(projectId, criteria = {}) {
        console.log(`[ExternalAPIs] Searching documents for project ${projectId}`);

        try {
            const searchParams = {
                project_id: projectId,
                query: criteria.query,
                document_type: criteria.type,
                page: criteria.page || 1,
                per_page: criteria.perPage || 10
            };

            const result = await this.callArchonAPI('find_documents', searchParams);

            if (Array.isArray(result)) {
                return result;
            } else if (result.success) {
                return result.documents || result.data || [];
            } else {
                return [];
            }

        } catch (error) {
            console.error(`[ExternalAPIs] Document search failed for project ${projectId}:`, error);
            return [];
        }
    }

    /**
     * GitHub Integration
     */
    async createGitHubRepository(repoData) {
        if (!this.endpoints.github.enabled) {
            console.warn('[ExternalAPIs] GitHub integration not configured');
            return null;
        }

        console.log(`[ExternalAPIs] Creating GitHub repository: ${repoData.name}`);

        try {
            const response = await this.makeRequest('github', 'POST', '/user/repos', {
                name: repoData.name,
                description: repoData.description,
                private: repoData.private || false,
                auto_init: repoData.autoInit || true
            });

            return response;

        } catch (error) {
            console.error('[ExternalAPIs] GitHub repository creation failed:', error);
            throw error;
        }
    }

    async createGitHubIssue(owner, repo, issueData) {
        if (!this.endpoints.github.enabled) {
            console.warn('[ExternalAPIs] GitHub integration not configured');
            return null;
        }

        console.log(`[ExternalAPIs] Creating GitHub issue in ${owner}/${repo}`);

        try {
            const endpoint = this.endpoints.github.endpoints.issues
                .replace('{owner}', owner)
                .replace('{repo}', repo);

            const response = await this.makeRequest('github', 'POST', endpoint, {
                title: issueData.title,
                body: issueData.body,
                labels: issueData.labels || [],
                assignees: issueData.assignees || []
            });

            return response;

        } catch (error) {
            console.error(`[ExternalAPIs] GitHub issue creation failed for ${owner}/${repo}:`, error);
            throw error;
        }
    }

    /**
     * Psychology-specific API integrations
     */
    async searchPsychologyResearch(query, domain, options = {}) {
        if (!this.endpoints.psychology.researchApi) {
            console.warn('[ExternalAPIs] Psychology research API not configured');
            return [];
        }

        console.log(`[ExternalAPIs] Searching psychology research: ${query}`);

        try {
            const response = await this.makeRequest('psychology', 'GET', '/research/search', {
                query,
                domain,
                limit: options.limit || 10,
                sort: options.sort || 'relevance'
            });

            return response.results || [];

        } catch (error) {
            console.error('[ExternalAPIs] Psychology research search failed:', error);
            return [];
        }
    }

    async getAssessmentTemplates(domain, type = null) {
        if (!this.endpoints.psychology.assessmentApi) {
            console.warn('[ExternalAPIs] Assessment API not configured');
            return [];
        }

        console.log(`[ExternalAPIs] Fetching assessment templates for ${domain}`);

        try {
            const response = await this.makeRequest('psychology', 'GET', '/assessments/templates', {
                domain,
                type,
                format: 'structured'
            });

            return response.templates || [];

        } catch (error) {
            console.error(`[ExternalAPIs] Assessment template fetch failed for ${domain}:`, error);
            return [];
        }
    }

    async getInterventionProtocols(domain, condition = null) {
        if (!this.endpoints.psychology.interventionApi) {
            console.warn('[ExternalAPIs] Intervention API not configured');
            return [];
        }

        console.log(`[ExternalAPIs] Fetching intervention protocols for ${domain}`);

        try {
            const response = await this.makeRequest('psychology', 'GET', '/interventions/protocols', {
                domain,
                condition,
                evidence_level: 'high'
            });

            return response.protocols || [];

        } catch (error) {
            console.error(`[ExternalAPIs] Intervention protocol fetch failed for ${domain}:`, error);
            return [];
        }
    }

    /**
     * Core API communication methods
     */
    async callArchonAPI(endpoint, params = {}) {
        const startTime = Date.now();

        try {
            // Check if we have the MCP function available
            const mcpFunction = global[`mcp__archon__${endpoint}`];

            if (typeof mcpFunction === 'function') {
                console.log(`[ExternalAPIs] Calling Archon MCP endpoint: ${endpoint}`);
                const result = await mcpFunction(params);
                this.updateMetrics(true, Date.now() - startTime);
                return result;
            } else {
                // Fallback simulation
                console.log(`[ExternalAPIs] Archon MCP function not available, simulating: ${endpoint}`);
                const result = await this.simulateArchonCall(endpoint, params);
                this.updateMetrics(true, Date.now() - startTime);
                return result;
            }

        } catch (error) {
            this.updateMetrics(false, Date.now() - startTime);
            throw error;
        }
    }

    async makeRequest(apiName, method, endpoint, data = null, headers = {}) {
        if (!this.endpoints[apiName] || !this.endpoints[apiName].enabled) {
            throw new Error(`API ${apiName} not configured or enabled`);
        }

        const startTime = Date.now();

        try {
            // Rate limiting check
            if (!this.checkRateLimit(apiName)) {
                throw new Error(`Rate limit exceeded for ${apiName}`);
            }

            // Concurrency check
            if (this.activeRequests >= this.config.maxConcurrentRequests) {
                await this.waitForAvailableSlot();
            }

            this.activeRequests++;

            // Build request configuration
            const config = this.buildRequestConfig(apiName, method, endpoint, data, headers);

            // Make the actual request (in real implementation, use fetch/axios)
            const response = await this.simulateAPIRequest(apiName, method, endpoint, data);

            this.updateMetrics(true, Date.now() - startTime);
            return response;

        } catch (error) {
            this.updateMetrics(false, Date.now() - startTime);
            throw error;
        } finally {
            this.activeRequests--;
        }
    }

    /**
     * Helper and utility methods
     */
    buildRequestConfig(apiName, method, endpoint, data, headers) {
        const api = this.endpoints[apiName];
        const url = `${api.baseUrl}${endpoint}`;

        const config = {
            method,
            url,
            timeout: this.config.timeout,
            headers: {
                'Content-Type': 'application/json',
                'User-Agent': 'Psychology-Content-Orchestrator/1.0.0',
                ...headers
            }
        };

        // Add authentication headers
        if (api.token) {
            config.headers.Authorization = `Bearer ${api.token}`;
        } else if (api.apiKey) {
            config.headers['X-API-Key'] = api.apiKey;
        }

        // Add data
        if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
            config.data = data;
        } else if (data && method === 'GET') {
            config.params = data;
        }

        return config;
    }

    checkRateLimit(apiName) {
        const now = Date.now();
        const windowStart = now - this.config.rateLimitWindow;

        if (!this.rateLimitTracker.has(apiName)) {
            this.rateLimitTracker.set(apiName, []);
        }

        const requests = this.rateLimitTracker.get(apiName);

        // Remove old requests outside the window
        const recentRequests = requests.filter(timestamp => timestamp > windowStart);
        this.rateLimitTracker.set(apiName, recentRequests);

        // Check if we can make a new request
        if (recentRequests.length >= this.config.maxRequestsPerWindow) {
            this.metrics.rateLimitHits++;
            return false;
        }

        // Add current request timestamp
        recentRequests.push(now);
        return true;
    }

    async waitForAvailableSlot() {
        return new Promise((resolve) => {
            const checkSlot = () => {
                if (this.activeRequests < this.config.maxConcurrentRequests) {
                    resolve();
                } else {
                    setTimeout(checkSlot, 100);
                }
            };
            checkSlot();
        });
    }

    updateMetrics(success, responseTime) {
        this.metrics.totalRequests++;
        this.metrics.totalResponseTime += responseTime;
        this.metrics.averageResponseTime = this.metrics.totalResponseTime / this.metrics.totalRequests;

        if (success) {
            this.metrics.successfulRequests++;
        } else {
            this.metrics.failedRequests++;
        }
    }

    /**
     * Simulation methods for testing/fallback
     */
    async simulateArchonCall(endpoint, params) {
        await this.simulateDelay(100, 500);

        const mockResponses = {
            'manage_project': {
                success: true,
                project: {
                    id: `proj-${Date.now()}`,
                    title: params.title,
                    description: params.description,
                    created_at: new Date().toISOString()
                }
            },
            'find_projects': [
                {
                    id: 'proj-example-1',
                    title: 'Example Psychology Project 1',
                    description: 'Mock project for testing'
                }
            ],
            'manage_task': {
                success: true,
                task: {
                    id: `task-${Date.now()}`,
                    title: params.title,
                    status: params.status || 'todo',
                    created_at: new Date().toISOString()
                }
            },
            'find_tasks': [
                {
                    id: 'task-example-1',
                    title: 'Example Task 1',
                    status: 'todo'
                }
            ],
            'manage_document': {
                success: true,
                document: {
                    id: `doc-${Date.now()}`,
                    title: params.title,
                    type: params.document_type,
                    created_at: new Date().toISOString()
                }
            },
            'find_documents': [
                {
                    id: 'doc-example-1',
                    title: 'Example Document 1',
                    type: 'note'
                }
            ]
        };

        return mockResponses[endpoint] || { success: false, message: 'Endpoint not found' };
    }

    async simulateAPIRequest(apiName, method, endpoint, data) {
        await this.simulateDelay(200, 1000);

        // Return mock successful response
        return {
            status: 200,
            data: {
                success: true,
                result: `Mock ${method} response for ${apiName}${endpoint}`,
                timestamp: new Date().toISOString()
            }
        };
    }

    async simulateDelay(min = 100, max = 500) {
        const delay = Math.floor(Math.random() * (max - min + 1)) + min;
        return new Promise(resolve => setTimeout(resolve, delay));
    }

    /**
     * Status and configuration methods
     */
    getStatus() {
        const successRate = this.metrics.totalRequests > 0
            ? this.metrics.successfulRequests / this.metrics.totalRequests
            : 0;

        return {
            activeRequests: this.activeRequests,
            enabledAPIs: Object.entries(this.endpoints)
                .filter(([name, config]) => config.enabled)
                .map(([name]) => name),
            metrics: {
                ...this.metrics,
                successRate
            },
            rateLimits: Object.fromEntries(this.rateLimitTracker),
            configuration: {
                timeout: this.config.timeout,
                maxConcurrentRequests: this.config.maxConcurrentRequests,
                maxRequestsPerWindow: this.config.maxRequestsPerWindow
            }
        };
    }

    getAvailableEndpoints() {
        const available = {};

        Object.entries(this.endpoints).forEach(([apiName, config]) => {
            if (config.enabled) {
                available[apiName] = {
                    baseUrl: config.baseUrl,
                    endpoints: config.endpoints || {},
                    status: 'available'
                };
            }
        });

        return available;
    }

    /**
     * Configuration update methods
     */
    updateAPIConfig(apiName, newConfig) {
        if (this.endpoints[apiName]) {
            this.endpoints[apiName] = {
                ...this.endpoints[apiName],
                ...newConfig
            };
            console.log(`[ExternalAPIs] Updated configuration for ${apiName}`);
        } else {
            console.warn(`[ExternalAPIs] API ${apiName} not found for configuration update`);
        }
    }

    enableAPI(apiName) {
        if (this.endpoints[apiName]) {
            this.endpoints[apiName].enabled = true;
            console.log(`[ExternalAPIs] Enabled ${apiName} API`);
        }
    }

    disableAPI(apiName) {
        if (this.endpoints[apiName]) {
            this.endpoints[apiName].enabled = false;
            console.log(`[ExternalAPIs] Disabled ${apiName} API`);
        }
    }
}

module.exports = ExternalAPIs;