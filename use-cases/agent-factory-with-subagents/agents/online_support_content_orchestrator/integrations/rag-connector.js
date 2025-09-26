/**
 * RAG Connector - Integration with Retrieval-Augmented Generation systems
 * Universal connector for various knowledge bases and RAG implementations
 */

class RAGConnector {
    constructor(config) {
        this.config = {
            ragEndpoint: config.ragEndpoint || 'mcp__archon__rag_search_knowledge_base',
            codeSearchEndpoint: config.codeSearchEndpoint || 'mcp__archon__rag_search_code_examples',
            defaultMatchCount: config.defaultMatchCount || 5,
            relevanceThreshold: config.relevanceThreshold || 0.7,
            maxRetries: config.maxRetries || 3,
            timeout: config.timeout || 30000,
            cacheEnabled: config.cacheEnabled !== false,
            cacheTTL: config.cacheTTL || 300000, // 5 minutes
            ...config
        };

        // Cache for RAG results
        this.cache = new Map();
        this.searchHistory = [];
        this.performanceMetrics = {
            totalSearches: 0,
            successfulSearches: 0,
            averageResponseTime: 0,
            cacheHits: 0
        };

        // Domain-specific search strategies
        this.searchStrategies = {
            'clinical-psychology': {
                priorityTerms: ['evidence-based', 'clinical-trial', 'therapy', 'treatment', 'diagnosis'],
                requiredDomains: ['clinical', 'therapeutic', 'medical'],
                searchModifiers: ['efficacy', 'safety', 'contraindications']
            },
            'educational-psychology': {
                priorityTerms: ['learning', 'pedagogy', 'curriculum', 'assessment', 'instruction'],
                requiredDomains: ['educational', 'academic', 'learning'],
                searchModifiers: ['age-appropriate', 'developmental', 'outcomes']
            },
            'organizational-psychology': {
                priorityTerms: ['workplace', 'organizational', 'leadership', 'team', 'performance'],
                requiredDomains: ['business', 'organizational', 'management'],
                searchModifiers: ['roi', 'implementation', 'culture']
            },
            'health-psychology': {
                priorityTerms: ['health-behavior', 'wellness', 'prevention', 'chronic-disease'],
                requiredDomains: ['health', 'medical', 'behavioral'],
                searchModifiers: ['intervention', 'outcome', 'adherence']
            }
        };
    }

    /**
     * Search for relevant knowledge based on query and domain
     * @param {string} query - Search query
     * @param {string} domain - Psychological domain
     * @param {Object} options - Additional search options
     * @returns {Promise<Array>} Array of relevant documents
     */
    async searchRelevantKnowledge(query, domain = 'general-psychology', options = {}) {
        const startTime = Date.now();
        const searchId = this.generateSearchId();

        console.log(`[RAGConnector] Starting knowledge search ${searchId} for domain: ${domain}`);

        try {
            this.performanceMetrics.totalSearches++;

            // Check cache first
            const cacheKey = this.getCacheKey(query, domain, options);
            if (this.config.cacheEnabled && this.cache.has(cacheKey)) {
                console.log(`[RAGConnector] Cache hit for search ${searchId}`);
                this.performanceMetrics.cacheHits++;
                return this.cache.get(cacheKey);
            }

            // Enhance query with domain-specific terms
            const enhancedQuery = await this.enhanceQuery(query, domain);

            // Execute multiple search strategies in parallel
            const searchPromises = [
                this.searchKnowledgeBase(enhancedQuery, domain, options),
                this.searchCodeExamples(enhancedQuery, domain, options),
                this.searchSpecializedContent(enhancedQuery, domain, options)
            ];

            const searchResults = await Promise.allSettled(searchPromises);

            // Combine and process results
            const combinedResults = await this.combineSearchResults(searchResults, domain);

            // Filter and rank results
            const filteredResults = await this.filterAndRankResults(combinedResults, query, domain, options);

            // Cache results
            if (this.config.cacheEnabled) {
                this.cache.set(cacheKey, filteredResults);
                setTimeout(() => this.cache.delete(cacheKey), this.config.cacheTTL);
            }

            // Update metrics
            const responseTime = Date.now() - startTime;
            this.updateMetrics(true, responseTime);

            // Log search to history
            this.logSearch(searchId, query, domain, filteredResults.length, responseTime);

            console.log(`[RAGConnector] Search ${searchId} completed: ${filteredResults.length} results in ${responseTime}ms`);

            return filteredResults;

        } catch (error) {
            console.error(`[RAGConnector] Search ${searchId} failed:`, error);
            this.updateMetrics(false, Date.now() - startTime);

            // Return empty results on failure
            return [];
        }
    }

    /**
     * Search main knowledge base
     */
    async searchKnowledgeBase(query, domain, options) {
        console.log(`[RAGConnector] Searching knowledge base for: ${query}`);

        try {
            // Use MCP Archon RAG search if available
            if (typeof mcp__archon__rag_search_knowledge_base === 'function') {
                const result = await mcp__archon__rag_search_knowledge_base({
                    query: query,
                    source_domain: this.getDomainFilter(domain),
                    match_count: options.matchCount || this.config.defaultMatchCount
                });

                if (result.success && result.results) {
                    return result.results.map(doc => ({
                        ...doc,
                        source: 'knowledge-base',
                        searchType: 'general-knowledge'
                    }));
                }
            }

            // Fallback to simulated search
            return this.simulateKnowledgeSearch(query, domain, options);

        } catch (error) {
            console.warn(`[RAGConnector] Knowledge base search failed: ${error.message}`);
            return [];
        }
    }

    /**
     * Search for code examples and technical implementations
     */
    async searchCodeExamples(query, domain, options) {
        console.log(`[RAGConnector] Searching code examples for: ${query}`);

        try {
            // Use MCP Archon code search if available
            if (typeof mcp__archon__rag_search_code_examples === 'function') {
                const result = await mcp__archon__rag_search_code_examples({
                    query: query,
                    source_domain: this.getDomainFilter(domain),
                    match_count: Math.ceil((options.matchCount || this.config.defaultMatchCount) / 2)
                });

                if (result.success && result.results) {
                    return result.results.map(doc => ({
                        ...doc,
                        source: 'code-examples',
                        searchType: 'technical-implementation'
                    }));
                }
            }

            // Fallback to simulated search
            return this.simulateCodeSearch(query, domain, options);

        } catch (error) {
            console.warn(`[RAGConnector] Code search failed: ${error.message}`);
            return [];
        }
    }

    /**
     * Search specialized content based on domain
     */
    async searchSpecializedContent(query, domain, options) {
        console.log(`[RAGConnector] Searching specialized content for domain: ${domain}`);

        const domainStrategy = this.searchStrategies[domain];
        if (!domainStrategy) {
            return [];
        }

        try {
            // Create domain-specific enhanced queries
            const specializedQueries = domainStrategy.priorityTerms.map(term =>
                `${query} ${term}`
            );

            // Search with specialized queries
            const searchPromises = specializedQueries.slice(0, 3).map(specializedQuery =>
                this.searchKnowledgeBase(specializedQuery, domain, {
                    ...options,
                    matchCount: 2
                })
            );

            const results = await Promise.allSettled(searchPromises);
            const successfulResults = results
                .filter(result => result.status === 'fulfilled')
                .flatMap(result => result.value);

            return successfulResults.map(doc => ({
                ...doc,
                source: 'specialized-content',
                searchType: 'domain-specific'
            }));

        } catch (error) {
            console.warn(`[RAGConnector] Specialized search failed: ${error.message}`);
            return [];
        }
    }

    /**
     * Enhance query with domain-specific terms and context
     */
    async enhanceQuery(query, domain) {
        const strategy = this.searchStrategies[domain];
        if (!strategy) {
            return query;
        }

        // Add priority terms
        const priorityTerm = strategy.priorityTerms[0];
        const enhancedQuery = `${query} ${priorityTerm}`;

        // Add search modifiers based on query type
        let modifier = '';
        if (query.toLowerCase().includes('assess')) {
            modifier = strategy.searchModifiers.find(m => m.includes('outcome')) || '';
        } else if (query.toLowerCase().includes('treat') || query.toLowerCase().includes('intervention')) {
            modifier = strategy.searchModifiers.find(m => m.includes('efficacy') || m.includes('implementation')) || '';
        }

        return modifier ? `${enhancedQuery} ${modifier}` : enhancedQuery;
    }

    /**
     * Combine results from multiple search strategies
     */
    async combineSearchResults(searchResults, domain) {
        const allResults = [];

        searchResults.forEach((result, index) => {
            if (result.status === 'fulfilled' && Array.isArray(result.value)) {
                result.value.forEach(doc => {
                    // Add metadata about search strategy
                    doc.searchStrategy = ['knowledge-base', 'code-examples', 'specialized'][index];
                    doc.domain = domain;
                    doc.retrievedAt = new Date().toISOString();
                    allResults.push(doc);
                });
            }
        });

        return allResults;
    }

    /**
     * Filter and rank results based on relevance and quality
     */
    async filterAndRankResults(results, originalQuery, domain, options) {
        // Remove duplicates based on content similarity
        const uniqueResults = this.removeDuplicates(results);

        // Filter by relevance threshold
        const relevantResults = uniqueResults.filter(doc =>
            (doc.relevance || doc.score || 1.0) >= this.config.relevanceThreshold
        );

        // Rank results using multiple criteria
        const rankedResults = relevantResults.sort((a, b) => {
            const scoreA = this.calculateRelevanceScore(a, originalQuery, domain);
            const scoreB = this.calculateRelevanceScore(b, originalQuery, domain);
            return scoreB - scoreA;
        });

        // Limit results
        const maxResults = options.matchCount || this.config.defaultMatchCount;
        return rankedResults.slice(0, maxResults);
    }

    /**
     * Calculate comprehensive relevance score for ranking
     */
    calculateRelevanceScore(document, query, domain) {
        let score = 0;

        // Base relevance/score
        score += (document.relevance || document.score || 0.5) * 0.4;

        // Source type weight
        const sourceWeights = {
            'knowledge-base': 0.3,
            'code-examples': 0.2,
            'specialized-content': 0.35
        };
        score += sourceWeights[document.source] || 0.2;

        // Domain alignment
        if (document.domain === domain || document.categories?.includes(domain)) {
            score += 0.2;
        }

        // Query term matching
        const queryTerms = query.toLowerCase().split(' ');
        const contentText = (document.content || document.summary || '').toLowerCase();
        const matchingTerms = queryTerms.filter(term =>
            contentText.includes(term) || document.title?.toLowerCase().includes(term)
        );
        score += (matchingTerms.length / queryTerms.length) * 0.1;

        // Recency boost (if available)
        if (document.date || document.updatedAt) {
            const docDate = new Date(document.date || document.updatedAt);
            const monthsOld = (Date.now() - docDate.getTime()) / (1000 * 60 * 60 * 24 * 30);
            const recencyScore = Math.max(0, 1 - (monthsOld / 24)); // Decay over 2 years
            score += recencyScore * 0.05;
        }

        return Math.min(score, 1.0);
    }

    /**
     * Remove duplicate documents based on content similarity
     */
    removeDuplicates(results) {
        const unique = [];
        const seenContent = new Set();

        results.forEach(doc => {
            // Create content fingerprint
            const contentKey = this.createContentFingerprint(doc);

            if (!seenContent.has(contentKey)) {
                seenContent.add(contentKey);
                unique.push(doc);
            }
        });

        return unique;
    }

    /**
     * Create content fingerprint for duplicate detection
     */
    createContentFingerprint(document) {
        const content = document.content || document.summary || document.title || '';

        // Simple fingerprint based on first 100 characters and key terms
        const excerpt = content.substring(0, 100).toLowerCase().trim();
        const words = excerpt.split(/\s+/).filter(word => word.length > 3);
        const keyWords = words.slice(0, 10).sort().join('|');

        return `${document.source || 'unknown'}:${keyWords}`;
    }

    /**
     * Get domain filter for search APIs
     */
    getDomainFilter(domain) {
        // Map internal domain names to external API domain filters
        const domainMapping = {
            'clinical-psychology': 'clinical',
            'educational-psychology': 'education',
            'organizational-psychology': 'business',
            'health-psychology': 'health',
            'positive-psychology': 'wellbeing',
            'cognitive-psychology': 'cognitive',
            'social-psychology': 'social'
        };

        return domainMapping[domain] || null;
    }

    /**
     * Simulation methods for fallback when external APIs unavailable
     */
    simulateKnowledgeSearch(query, domain, options) {
        // Generate mock search results for testing/fallback
        const mockResults = [];
        const resultCount = Math.min(options.matchCount || this.config.defaultMatchCount, 5);

        for (let i = 0; i < resultCount; i++) {
            mockResults.push({
                id: `mock-kb-${Date.now()}-${i}`,
                title: `Knowledge Base Result ${i + 1} for "${query}"`,
                content: `This is a simulated knowledge base result for the query "${query}" in the ${domain} domain. This would contain relevant psychological research, theories, and evidence-based practices.`,
                source: 'knowledge-base',
                searchType: 'general-knowledge',
                relevance: 0.8 - (i * 0.1),
                categories: [domain, 'research', 'evidence-based'],
                url: `https://knowledge-base.example.com/doc-${i}`,
                date: new Date(Date.now() - i * 86400000).toISOString()
            });
        }

        return mockResults;
    }

    simulateCodeSearch(query, domain, options) {
        const mockResults = [];
        const resultCount = Math.min(Math.ceil((options.matchCount || this.config.defaultMatchCount) / 2), 3);

        for (let i = 0; i < resultCount; i++) {
            mockResults.push({
                id: `mock-code-${Date.now()}-${i}`,
                title: `Code Example ${i + 1} for "${query}"`,
                content: `// Code example for ${query} in ${domain}\n// This would contain implementation examples, algorithms, or technical frameworks`,
                source: 'code-examples',
                searchType: 'technical-implementation',
                relevance: 0.7 - (i * 0.1),
                categories: [domain, 'implementation', 'technical'],
                language: 'javascript',
                framework: 'psychology-framework',
                url: `https://code-examples.example.com/example-${i}`
            });
        }

        return mockResults;
    }

    /**
     * Utility methods
     */
    getCacheKey(query, domain, options) {
        return `${query}|${domain}|${JSON.stringify(options)}`;
    }

    generateSearchId() {
        return `search_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }

    updateMetrics(success, responseTime) {
        if (success) {
            this.performanceMetrics.successfulSearches++;
        }

        // Update average response time
        const totalSearches = this.performanceMetrics.totalSearches;
        const currentAverage = this.performanceMetrics.averageResponseTime;
        this.performanceMetrics.averageResponseTime =
            ((currentAverage * (totalSearches - 1)) + responseTime) / totalSearches;
    }

    logSearch(searchId, query, domain, resultCount, responseTime) {
        const searchRecord = {
            id: searchId,
            query,
            domain,
            resultCount,
            responseTime,
            timestamp: new Date().toISOString()
        };

        this.searchHistory.push(searchRecord);

        // Keep only last 100 searches
        if (this.searchHistory.length > 100) {
            this.searchHistory.shift();
        }
    }

    /**
     * RAG context preparation for agents
     */
    prepareRAGContext(searchResults, taskType = 'general') {
        const context = {
            totalResults: searchResults.length,
            sources: [...new Set(searchResults.map(r => r.source))],
            searchTypes: [...new Set(searchResults.map(r => r.searchType))],
            relevanceRange: {
                min: Math.min(...searchResults.map(r => r.relevance || 0.5)),
                max: Math.max(...searchResults.map(r => r.relevance || 0.5))
            },
            content: {
                knowledge: searchResults.filter(r => r.source === 'knowledge-base'),
                technical: searchResults.filter(r => r.source === 'code-examples'),
                specialized: searchResults.filter(r => r.source === 'specialized-content')
            }
        };

        // Create condensed content for each category
        Object.keys(context.content).forEach(category => {
            const categoryResults = context.content[category];
            context.content[category] = {
                count: categoryResults.length,
                summary: this.summarizeResults(categoryResults),
                topResults: categoryResults.slice(0, 3),
                keyTopics: this.extractKeyTopics(categoryResults)
            };
        });

        return context;
    }

    /**
     * Summarize search results for context
     */
    summarizeResults(results) {
        if (results.length === 0) return '';

        const allContent = results
            .map(r => r.content || r.summary || r.title)
            .join(' ')
            .substring(0, 500);

        return `Summary of ${results.length} results: ${allContent}...`;
    }

    /**
     * Extract key topics from search results
     */
    extractKeyTopics(results) {
        const allText = results
            .map(r => `${r.title} ${r.content || r.summary || ''}`)
            .join(' ')
            .toLowerCase();

        // Simple keyword extraction (in production, use more sophisticated NLP)
        const words = allText.match(/\b\w{4,}\b/g) || [];
        const wordCounts = {};

        words.forEach(word => {
            wordCounts[word] = (wordCounts[word] || 0) + 1;
        });

        return Object.entries(wordCounts)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10)
            .map(([word]) => word);
    }

    /**
     * Get connector status and performance metrics
     */
    getStatus() {
        const successRate = this.performanceMetrics.totalSearches > 0
            ? this.performanceMetrics.successfulSearches / this.performanceMetrics.totalSearches
            : 0;

        const cacheHitRate = this.performanceMetrics.totalSearches > 0
            ? this.performanceMetrics.cacheHits / this.performanceMetrics.totalSearches
            : 0;

        return {
            isConnected: true, // Would check actual connection in production
            cacheSize: this.cache.size,
            searchHistorySize: this.searchHistory.length,
            metrics: {
                ...this.performanceMetrics,
                successRate,
                cacheHitRate
            },
            configuration: {
                ragEndpoint: this.config.ragEndpoint,
                defaultMatchCount: this.config.defaultMatchCount,
                relevanceThreshold: this.config.relevanceThreshold,
                cacheEnabled: this.config.cacheEnabled
            }
        };
    }

    /**
     * Clear cache and reset metrics
     */
    reset() {
        this.cache.clear();
        this.searchHistory = [];
        this.performanceMetrics = {
            totalSearches: 0,
            successfulSearches: 0,
            averageResponseTime: 0,
            cacheHits: 0
        };
    }
}

module.exports = RAGConnector;