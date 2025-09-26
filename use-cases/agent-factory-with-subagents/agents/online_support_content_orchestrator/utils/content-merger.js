/**
 * Content Merger - Intelligent integration of multi-agent outputs
 * Handles the synthesis and merging of content from multiple specialized agents
 */

class ContentMerger {
    constructor(config) {
        this.config = {
            domain: config.domain || 'general-psychology',
            integrationStrategy: config.integrationStrategy || 'standard',
            qualityThreshold: config.qualityThreshold || 0.8,
            conflictResolution: config.conflictResolution || 'weighted-consensus',
            outputFormat: config.outputFormat || 'comprehensive',
            preserveAgentAttribution: config.preserveAgentAttribution !== false,
            ...config
        };

        // Integration strategies for different content types
        this.integrationStrategies = {
            'standard': {
                priority: ['research', 'architect', 'nlp-generator', 'quality-guardian'],
                conflictResolution: 'weighted-consensus',
                outputStructure: 'modular'
            },
            'clinical-protocols': {
                priority: ['research', 'clinical-expert', 'test-generator', 'quality-guardian'],
                conflictResolution: 'expert-hierarchy',
                outputStructure: 'protocol-based',
                mandatoryValidation: true
            },
            'educational-curriculum': {
                priority: ['research', 'pedagogy-expert', 'curriculum-designer', 'assessment-creator'],
                conflictResolution: 'pedagogical-consensus',
                outputStructure: 'progressive-learning'
            },
            'organizational-systems': {
                priority: ['research', 'organizational-expert', 'architect', 'change-management'],
                conflictResolution: 'stakeholder-alignment',
                outputStructure: 'implementation-focused'
            },
            'holistic-wellbeing': {
                priority: ['research', 'wellness-expert', 'technique-designer', 'nlp-generator'],
                conflictResolution: 'holistic-integration',
                outputStructure: 'experience-journey'
            }
        };

        // Content structure templates
        this.outputTemplates = {
            'comprehensive': {
                sections: [
                    'executive-summary',
                    'theoretical-foundation',
                    'assessment-framework',
                    'intervention-protocols',
                    'implementation-guide',
                    'quality-assurance',
                    'resources-references'
                ]
            },
            'modular': {
                sections: [
                    'overview',
                    'modules',
                    'assessments',
                    'resources',
                    'implementation'
                ]
            },
            'protocol-based': {
                sections: [
                    'clinical-overview',
                    'assessment-protocol',
                    'treatment-protocol',
                    'safety-considerations',
                    'outcome-measures',
                    'supervision-guidelines'
                ]
            },
            'progressive-learning': {
                sections: [
                    'learning-objectives',
                    'prerequisite-knowledge',
                    'learning-modules',
                    'assessment-strategy',
                    'progress-tracking',
                    'support-resources'
                ]
            }
        };

        // Conflict resolution strategies
        this.conflictResolvers = {
            'weighted-consensus': this.resolveByWeightedConsensus.bind(this),
            'expert-hierarchy': this.resolveByExpertHierarchy.bind(this),
            'evidence-priority': this.resolveByEvidencePriority.bind(this),
            'stakeholder-alignment': this.resolveByStakeholderAlignment.bind(this),
            'latest-consensus': this.resolveByLatestConsensus.bind(this)
        };

        this.mergeHistory = [];
        this.qualityMetrics = [];
    }

    /**
     * Main content merging method
     * @param {Object} executionResults - Results from all agent executions
     * @param {Object} context - Merge context and configuration
     * @returns {Object} Integrated content package
     */
    async mergeResults(executionResults, context = {}) {
        const mergeId = this.generateMergeId();
        const startTime = Date.now();

        console.log(`[ContentMerger] Starting content merge ${mergeId}`);

        try {
            // Extract and organize agent outputs
            const agentOutputs = await this.extractAgentOutputs(executionResults);

            // Analyze content for conflicts and gaps
            const contentAnalysis = await this.analyzeContent(agentOutputs);

            // Resolve conflicts between agent outputs
            const resolvedContent = await this.resolveConflicts(agentOutputs, contentAnalysis, context);

            // Structure content according to domain and strategy
            const structuredContent = await this.structureContent(resolvedContent, context);

            // Enhance content with cross-references and integration
            const enhancedContent = await this.enhanceIntegration(structuredContent, context);

            // Validate integrated content
            const validationResult = await this.validateIntegratedContent(enhancedContent, context);

            // Generate metadata and attribution
            const finalContent = await this.addMetadataAndAttribution(enhancedContent, agentOutputs, context);

            const mergeTime = Date.now() - startTime;
            this.recordMergeMetrics(mergeId, agentOutputs, finalContent, mergeTime, validationResult);

            console.log(`[ContentMerger] Content merge ${mergeId} completed in ${mergeTime}ms`);

            return {
                content: finalContent,
                metadata: {
                    mergeId,
                    mergeTime,
                    agentsInvolved: Object.keys(agentOutputs),
                    integrationStrategy: this.config.integrationStrategy,
                    qualityScore: validationResult.score,
                    conflictsResolved: contentAnalysis.conflicts.length,
                    domain: context.domain || this.config.domain
                },
                validation: validationResult,
                sources: this.generateSourceAttribution(agentOutputs)
            };

        } catch (error) {
            console.error(`[ContentMerger] Merge ${mergeId} failed:`, error);
            throw new Error(`Content merge failed: ${error.message}`);
        }
    }

    /**
     * Extract and organize outputs from agent execution results
     */
    async extractAgentOutputs(executionResults) {
        const agentOutputs = {};

        // Process each phase and extract agent contributions
        Object.entries(executionResults).forEach(([phaseName, phaseResult]) => {
            if (phaseResult.success && phaseResult.results) {
                phaseResult.results.forEach(taskResult => {
                    if (taskResult.success && taskResult.agentUsed) {
                        const agentName = taskResult.agentUsed;

                        if (!agentOutputs[agentName]) {
                            agentOutputs[agentName] = {
                                agent: agentName,
                                contributions: [],
                                totalOutputs: 0,
                                averageQuality: 0,
                                phases: []
                            };
                        }

                        agentOutputs[agentName].contributions.push({
                            phase: phaseName,
                            content: taskResult.result,
                            metadata: taskResult.metadata,
                            timestamp: new Date().toISOString()
                        });

                        agentOutputs[agentName].phases.push(phaseName);
                        agentOutputs[agentName].totalOutputs++;

                        // Update quality metrics
                        if (taskResult.metadata && taskResult.metadata.qualityScore) {
                            const currentAvg = agentOutputs[agentName].averageQuality;
                            const newQuality = taskResult.metadata.qualityScore;
                            const count = agentOutputs[agentName].totalOutputs;

                            agentOutputs[agentName].averageQuality =
                                ((currentAvg * (count - 1)) + newQuality) / count;
                        }
                    }
                });
            }
        });

        return agentOutputs;
    }

    /**
     * Analyze content for conflicts, overlaps, and gaps
     */
    async analyzeContent(agentOutputs) {
        console.log(`[ContentMerger] Analyzing content from ${Object.keys(agentOutputs).length} agents`);

        const analysis = {
            conflicts: [],
            overlaps: [],
            gaps: [],
            consistencyScore: 0,
            coverage: {},
            qualityDistribution: {}
        };

        const allContributions = Object.values(agentOutputs).flatMap(agent => agent.contributions);

        // Detect conflicts
        analysis.conflicts = await this.detectConflicts(allContributions);

        // Detect overlaps
        analysis.overlaps = await this.detectOverlaps(allContributions);

        // Identify gaps
        analysis.gaps = await this.identifyGaps(allContributions);

        // Calculate consistency score
        analysis.consistencyScore = this.calculateConsistencyScore(analysis);

        // Analyze coverage by content type
        analysis.coverage = this.analyzeCoverage(allContributions);

        // Quality distribution analysis
        analysis.qualityDistribution = this.analyzeQualityDistribution(agentOutputs);

        return analysis;
    }

    /**
     * Resolve conflicts between agent outputs
     */
    async resolveConflicts(agentOutputs, contentAnalysis, context) {
        console.log(`[ContentMerger] Resolving ${contentAnalysis.conflicts.length} content conflicts`);

        if (contentAnalysis.conflicts.length === 0) {
            return agentOutputs;
        }

        const strategy = this.integrationStrategies[this.config.integrationStrategy] || this.integrationStrategies.standard;
        const resolver = this.conflictResolvers[strategy.conflictResolution] || this.conflictResolvers['weighted-consensus'];

        const resolvedOutputs = JSON.parse(JSON.stringify(agentOutputs)); // Deep clone

        for (const conflict of contentAnalysis.conflicts) {
            const resolution = await resolver(conflict, agentOutputs, context);

            // Apply resolution to affected contributions
            this.applyConflictResolution(resolvedOutputs, conflict, resolution);
        }

        return resolvedOutputs;
    }

    /**
     * Structure content according to domain-specific templates
     */
    async structureContent(resolvedContent, context) {
        console.log(`[ContentMerger] Structuring content for ${context.domain || this.config.domain}`);

        const strategy = this.integrationStrategies[this.config.integrationStrategy] || this.integrationStrategies.standard;
        const template = this.outputTemplates[strategy.outputStructure] || this.outputTemplates.comprehensive;

        const structuredContent = {
            structure: strategy.outputStructure,
            sections: {},
            navigation: [],
            crossReferences: {}
        };

        // Create sections based on template
        for (const sectionName of template.sections) {
            structuredContent.sections[sectionName] = await this.createSection(
                sectionName,
                resolvedContent,
                context
            );

            structuredContent.navigation.push({
                section: sectionName,
                title: this.getSectionTitle(sectionName),
                contentType: this.getSectionContentType(sectionName),
                order: template.sections.indexOf(sectionName)
            });
        }

        // Add cross-references between sections
        structuredContent.crossReferences = this.generateCrossReferences(structuredContent.sections);

        return structuredContent;
    }

    /**
     * Enhance content with integration features
     */
    async enhanceIntegration(structuredContent, context) {
        console.log(`[ContentMerger] Enhancing integration features`);

        const enhanced = JSON.parse(JSON.stringify(structuredContent));

        // Add integration elements
        enhanced.integrationFeatures = {
            // Coherence threads that connect related concepts across sections
            coherenceThreads: await this.generateCoherenceThreads(enhanced.sections),

            // Progressive disclosure for complex content
            progressiveDisclosure: await this.createProgressiveDisclosure(enhanced.sections),

            // Adaptive pathways based on user needs
            adaptivePathways: await this.generateAdaptivePathways(enhanced.sections, context),

            // Quality indicators and evidence levels
            qualityIndicators: await this.addQualityIndicators(enhanced.sections),

            // Interactive elements and engagement features
            interactiveElements: await this.createInteractiveElements(enhanced.sections)
        };

        // Enhance navigation with integration features
        enhanced.enhancedNavigation = await this.createEnhancedNavigation(
            enhanced.navigation,
            enhanced.integrationFeatures
        );

        return enhanced;
    }

    /**
     * Validate the integrated content package
     */
    async validateIntegratedContent(enhancedContent, context) {
        console.log(`[ContentMerger] Validating integrated content`);

        const validation = {
            score: 0,
            passed: true,
            issues: [],
            strengths: [],
            recommendations: []
        };

        // Completeness validation
        const completenessScore = this.validateCompleteness(enhancedContent);
        validation.score += completenessScore * 0.3;

        // Coherence validation
        const coherenceScore = this.validateCoherence(enhancedContent);
        validation.score += coherenceScore * 0.25;

        // Quality validation
        const qualityScore = this.validateOverallQuality(enhancedContent);
        validation.score += qualityScore * 0.25;

        // Domain alignment validation
        const alignmentScore = this.validateDomainAlignment(enhancedContent, context);
        validation.score += alignmentScore * 0.2;

        // Check if meets threshold
        if (validation.score < this.config.qualityThreshold) {
            validation.passed = false;
            validation.issues.push(`Overall quality score ${validation.score.toFixed(2)} below threshold ${this.config.qualityThreshold}`);
        }

        return validation;
    }

    /**
     * Add metadata and attribution information
     */
    async addMetadataAndAttribution(enhancedContent, agentOutputs, context) {
        const finalContent = JSON.parse(JSON.stringify(enhancedContent));

        // Add comprehensive metadata
        finalContent.metadata = {
            ...finalContent.metadata,
            created: new Date().toISOString(),
            domain: context.domain || this.config.domain,
            contentType: context.contentType || 'integrated-program',
            version: '1.0.0',
            orchestrator: {
                name: 'Psychology Content Orchestrator',
                version: '1.0.0',
                integrationStrategy: this.config.integrationStrategy
            },
            contributors: Object.keys(agentOutputs).map(agentName => ({
                agent: agentName,
                contributions: agentOutputs[agentName].totalOutputs,
                qualityScore: agentOutputs[agentName].averageQuality,
                phases: agentOutputs[agentName].phases
            })),
            contentMetrics: {
                totalSections: Object.keys(finalContent.sections).length,
                crossReferences: Object.keys(finalContent.crossReferences || {}).length,
                integrationFeatures: Object.keys(finalContent.integrationFeatures || {}).length
            }
        };

        // Add attribution if enabled
        if (this.config.preserveAgentAttribution) {
            finalContent.attribution = this.createDetailedAttribution(agentOutputs);
        }

        // Add usage guidelines
        finalContent.usageGuidelines = this.generateUsageGuidelines(finalContent, context);

        return finalContent;
    }

    /**
     * Conflict resolution strategies
     */
    async resolveByWeightedConsensus(conflict, agentOutputs, context) {
        // Weight agents by their quality scores and domain expertise
        const weights = this.calculateAgentWeights(conflict.involvedAgents, agentOutputs, context);

        // Find consensus based on weighted voting
        const weightedOptions = conflict.options.map(option => ({
            ...option,
            weightedScore: weights[option.agent] || 0.5
        }));

        const consensus = weightedOptions.reduce((best, current) =>
            current.weightedScore > best.weightedScore ? current : best
        );

        return {
            strategy: 'weighted-consensus',
            resolution: consensus,
            confidence: consensus.weightedScore,
            rationale: `Selected based on agent expertise and quality scores`
        };
    }

    async resolveByExpertHierarchy(conflict, agentOutputs, context) {
        // Define expert hierarchy for domain
        const hierarchy = this.getExpertHierarchy(context.domain || this.config.domain);

        // Select highest-ranking expert's input
        let bestOption = null;
        let bestRank = Infinity;

        conflict.options.forEach(option => {
            const rank = hierarchy.indexOf(option.agent);
            if (rank !== -1 && rank < bestRank) {
                bestRank = rank;
                bestOption = option;
            }
        });

        return {
            strategy: 'expert-hierarchy',
            resolution: bestOption || conflict.options[0],
            confidence: bestOption ? 0.9 : 0.5,
            rationale: `Selected based on domain expert hierarchy`
        };
    }

    async resolveByEvidencePriority(conflict, agentOutputs, context) {
        // Prioritize options with stronger evidence base
        const evidenceScored = conflict.options.map(option => ({
            ...option,
            evidenceScore: this.assessEvidenceStrength(option.content)
        }));

        const bestEvidence = evidenceScored.reduce((best, current) =>
            current.evidenceScore > best.evidenceScore ? current : best
        );

        return {
            strategy: 'evidence-priority',
            resolution: bestEvidence,
            confidence: bestEvidence.evidenceScore,
            rationale: `Selected based on strength of supporting evidence`
        };
    }

    /**
     * Helper methods for content analysis and processing
     */
    async detectConflicts(contributions) {
        const conflicts = [];

        // Simple conflict detection based on content similarity and disagreement
        // In production, this would use more sophisticated NLP analysis

        for (let i = 0; i < contributions.length; i++) {
            for (let j = i + 1; j < contributions.length; j++) {
                const similarity = this.calculateContentSimilarity(
                    contributions[i].content,
                    contributions[j].content
                );

                if (similarity > 0.7 && this.detectDisagreement(contributions[i], contributions[j])) {
                    conflicts.push({
                        type: 'content-disagreement',
                        involvedAgents: [contributions[i], contributions[j]],
                        options: [
                            { agent: contributions[i].phase, content: contributions[i].content },
                            { agent: contributions[j].phase, content: contributions[j].content }
                        ],
                        similarity,
                        severity: this.assessConflictSeverity(contributions[i], contributions[j])
                    });
                }
            }
        }

        return conflicts;
    }

    calculateContentSimilarity(content1, content2) {
        // Simple similarity calculation
        // In production, use more sophisticated methods
        if (!content1 || !content2) return 0;

        const str1 = JSON.stringify(content1).toLowerCase();
        const str2 = JSON.stringify(content2).toLowerCase();

        const words1 = str1.match(/\w+/g) || [];
        const words2 = str2.match(/\w+/g) || [];

        const intersection = words1.filter(word => words2.includes(word));
        const union = [...new Set([...words1, ...words2])];

        return intersection.length / union.length;
    }

    detectDisagreement(contrib1, contrib2) {
        // Simple disagreement detection
        // Look for contradictory keywords or opposite recommendations
        const content1 = JSON.stringify(contrib1.content).toLowerCase();
        const content2 = JSON.stringify(contrib2.content).toLowerCase();

        const contradictoryPairs = [
            ['recommend', 'not recommend'],
            ['effective', 'ineffective'],
            ['safe', 'unsafe'],
            ['approved', 'contraindicated']
        ];

        return contradictoryPairs.some(([pos, neg]) =>
            (content1.includes(pos) && content2.includes(neg)) ||
            (content1.includes(neg) && content2.includes(pos))
        );
    }

    generateMergeId() {
        return `merge_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }

    getSectionTitle(sectionName) {
        const titles = {
            'executive-summary': 'Executive Summary',
            'theoretical-foundation': 'Theoretical Foundation',
            'assessment-framework': 'Assessment Framework',
            'intervention-protocols': 'Intervention Protocols',
            'implementation-guide': 'Implementation Guide',
            'quality-assurance': 'Quality Assurance',
            'resources-references': 'Resources and References'
        };

        return titles[sectionName] || sectionName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    async createSection(sectionName, resolvedContent, context) {
        // Create section content by aggregating relevant agent contributions
        const relevantContributions = this.getRelevantContributions(sectionName, resolvedContent);

        return {
            title: this.getSectionTitle(sectionName),
            content: await this.synthesizeContributions(relevantContributions, sectionName),
            contributors: relevantContributions.map(c => c.agent),
            quality: this.calculateSectionQuality(relevantContributions),
            metadata: {
                created: new Date().toISOString(),
                contributionCount: relevantContributions.length,
                section: sectionName
            }
        };
    }

    getRelevantContributions(sectionName, resolvedContent) {
        // Map section names to relevant agent types and contributions
        const sectionMapping = {
            'executive-summary': ['research', 'architect', 'integrator'],
            'theoretical-foundation': ['research', 'domain-expert'],
            'assessment-framework': ['test-generator', 'psychometrician', 'quality-guardian'],
            'intervention-protocols': ['nlp-generator', 'technique-designer', 'clinical-expert'],
            'implementation-guide': ['architect', 'integrator', 'organizational-expert'],
            'quality-assurance': ['quality-guardian', 'clinical-expert'],
            'resources-references': ['research', 'domain-expert']
        };

        const relevantAgents = sectionMapping[sectionName] || Object.keys(resolvedContent);
        const contributions = [];

        Object.entries(resolvedContent).forEach(([agentName, agentData]) => {
            if (relevantAgents.includes(agentName)) {
                contributions.push(...agentData.contributions.map(c => ({
                    ...c,
                    agent: agentName
                })));
            }
        });

        return contributions;
    }

    async synthesizeContributions(contributions, sectionName) {
        // Synthesize multiple contributions into coherent section content
        // This is a simplified version - production would use more sophisticated synthesis

        const synthesized = {
            summary: `Synthesized content for ${sectionName} section`,
            mainPoints: [],
            details: {},
            recommendations: []
        };

        contributions.forEach(contrib => {
            // Extract key information from each contribution
            if (contrib.content) {
                synthesized.details[contrib.agent] = contrib.content;

                // Extract recommendations if present
                if (contrib.content.recommendations) {
                    synthesized.recommendations.push(...contrib.content.recommendations);
                }

                // Extract main points
                if (contrib.content.mainPoints || contrib.content.keyFindings) {
                    synthesized.mainPoints.push(...(contrib.content.mainPoints || contrib.content.keyFindings));
                }
            }
        });

        // Remove duplicates and synthesize
        synthesized.mainPoints = [...new Set(synthesized.mainPoints)];
        synthesized.recommendations = [...new Set(synthesized.recommendations)];

        return synthesized;
    }

    recordMergeMetrics(mergeId, agentOutputs, finalContent, mergeTime, validationResult) {
        const metrics = {
            mergeId,
            timestamp: new Date().toISOString(),
            agentCount: Object.keys(agentOutputs).length,
            totalContributions: Object.values(agentOutputs).reduce((sum, agent) => sum + agent.totalOutputs, 0),
            mergeTime,
            qualityScore: validationResult.score,
            integrationStrategy: this.config.integrationStrategy,
            finalSections: Object.keys(finalContent.sections).length
        };

        this.mergeHistory.push(metrics);
        this.qualityMetrics.push(validationResult.score);

        // Keep only last 100 merges
        if (this.mergeHistory.length > 100) {
            this.mergeHistory.shift();
        }

        if (this.qualityMetrics.length > 100) {
            this.qualityMetrics.shift();
        }
    }

    /**
     * Get merger status and performance metrics
     */
    getStatus() {
        const averageQuality = this.qualityMetrics.length > 0
            ? this.qualityMetrics.reduce((sum, score) => sum + score, 0) / this.qualityMetrics.length
            : 0;

        const averageMergeTime = this.mergeHistory.length > 0
            ? this.mergeHistory.reduce((sum, merge) => sum + merge.mergeTime, 0) / this.mergeHistory.length
            : 0;

        return {
            totalMerges: this.mergeHistory.length,
            averageQuality,
            averageMergeTime,
            integrationStrategy: this.config.integrationStrategy,
            conflictResolution: this.config.conflictResolution,
            qualityThreshold: this.config.qualityThreshold,
            recentMerges: this.mergeHistory.slice(-5),
            availableStrategies: Object.keys(this.integrationStrategies),
            availableTemplates: Object.keys(this.outputTemplates)
        };
    }
}

module.exports = ContentMerger;