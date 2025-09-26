/**
 * Quality Validator - Comprehensive content quality assessment
 * Validates psychological content against domain-specific standards and best practices
 */

class QualityValidator {
    constructor(config) {
        this.config = {
            domain: config.domain || 'general-psychology',
            threshold: config.threshold || 0.8,
            strictMode: config.strictMode || false,
            validationRules: config.validationRules || {},
            customValidators: config.customValidators || {},
            weightingScheme: config.weightingScheme || 'balanced',
            ...config
        };

        // Validation criteria weights for different domains
        this.domainWeights = {
            'clinical-psychology': {
                'evidence-quality': 0.25,
                'safety-assessment': 0.20,
                'clinical-accuracy': 0.20,
                'ethical-compliance': 0.15,
                'practical-applicability': 0.10,
                'completeness': 0.10
            },
            'educational-psychology': {
                'pedagogical-soundness': 0.25,
                'learning-alignment': 0.20,
                'age-appropriateness': 0.15,
                'assessment-validity': 0.15,
                'engagement-potential': 0.15,
                'accessibility': 0.10
            },
            'organizational-psychology': {
                'business-alignment': 0.20,
                'implementation-feasibility': 0.20,
                'stakeholder-value': 0.15,
                'change-management': 0.15,
                'measurement-framework': 0.15,
                'roi-potential': 0.15
            },
            'general-psychology': {
                'scientific-accuracy': 0.20,
                'evidence-base': 0.20,
                'ethical-standards': 0.15,
                'practical-utility': 0.15,
                'clarity-communication': 0.15,
                'completeness': 0.15
            }
        };

        // Validation rule sets
        this.validationRules = {
            'evidence-quality': {
                criteria: [
                    'peer-reviewed-sources',
                    'recent-research',
                    'methodological-rigor',
                    'effect-size-reporting',
                    'confidence-intervals'
                ],
                threshold: 0.75,
                weight: 1.0
            },
            'safety-assessment': {
                criteria: [
                    'contraindications-identified',
                    'risk-factors-assessed',
                    'safety-protocols',
                    'adverse-effects-documented',
                    'supervision-requirements'
                ],
                threshold: 0.90,
                weight: 1.0,
                mandatory: true
            },
            'ethical-compliance': {
                criteria: [
                    'informed-consent',
                    'confidentiality',
                    'professional-boundaries',
                    'cultural-sensitivity',
                    'do-no-harm'
                ],
                threshold: 0.85,
                weight: 1.0,
                mandatory: true
            },
            'pedagogical-soundness': {
                criteria: [
                    'learning-objectives',
                    'scaffolding',
                    'active-learning',
                    'feedback-mechanisms',
                    'transfer-support'
                ],
                threshold: 0.80,
                weight: 1.0
            },
            'clinical-accuracy': {
                criteria: [
                    'diagnostic-precision',
                    'treatment-protocols',
                    'outcome-measures',
                    'professional-standards',
                    'evidence-alignment'
                ],
                threshold: 0.85,
                weight: 1.0
            }
        };

        // Quality indicators and red flags
        this.qualityIndicators = {
            positive: [
                'evidence-based-recommendations',
                'clear-implementation-steps',
                'measurable-outcomes',
                'cultural-adaptations',
                'professional-validation',
                'pilot-testing-results',
                'user-feedback-integration',
                'continuous-improvement',
                'stakeholder-involvement',
                'interdisciplinary-input'
            ],
            negative: [
                'unsupported-claims',
                'methodological-flaws',
                'bias-indicators',
                'overgeneralization',
                'missing-disclaimers',
                'inadequate-safety-measures',
                'cultural-insensitivity',
                'outdated-practices',
                'conflicts-of-interest',
                'insufficient-documentation'
            ]
        };

        this.validationHistory = [];
        this.performanceMetrics = {
            totalValidations: 0,
            averageScore: 0,
            failureRate: 0,
            improvementRate: 0
        };
    }

    /**
     * Main content validation method
     * @param {Object} content - Content to validate
     * @param {Object} context - Validation context
     * @returns {Promise<Object>} Validation results
     */
    async validateContent(content, context = {}) {
        const validationId = this.generateValidationId();
        const startTime = Date.now();

        console.log(`[QualityValidator] Starting validation ${validationId} for domain: ${context.domain}`);

        try {
            this.performanceMetrics.totalValidations++;

            const validationContext = {
                domain: context.domain || this.config.domain,
                threshold: context.threshold || this.config.threshold,
                strictMode: context.strictMode || this.config.strictMode,
                workflowId: context.workflowId,
                contentType: this.inferContentType(content),
                ...context
            };

            // Multi-dimensional validation
            const validationResults = await this.performComprehensiveValidation(content, validationContext);

            // Calculate overall quality score
            const overallScore = this.calculateOverallScore(validationResults, validationContext);

            // Generate recommendations
            const recommendations = await this.generateRecommendations(validationResults, validationContext);

            // Determine pass/fail status
            const passed = overallScore >= validationContext.threshold &&
                this.checkMandatoryRequirements(validationResults);

            const validationTime = Date.now() - startTime;

            const finalResult = {
                validationId,
                passed,
                score: overallScore,
                threshold: validationContext.threshold,
                domain: validationContext.domain,
                contentType: validationContext.contentType,
                validationTime,
                detailedResults: validationResults,
                recommendations: recommendations,
                summary: this.generateValidationSummary(validationResults, overallScore, passed),
                metadata: {
                    timestamp: new Date().toISOString(),
                    validator: 'Psychology Quality Validator v1.0.0',
                    strictMode: validationContext.strictMode,
                    criteriaCount: Object.keys(validationResults).length
                }
            };

            // Record validation metrics
            this.recordValidationMetrics(validationId, finalResult);

            console.log(`[QualityValidator] Validation ${validationId} completed: ${passed ? 'PASSED' : 'FAILED'} (${overallScore.toFixed(2)})`);

            return finalResult;

        } catch (error) {
            console.error(`[QualityValidator] Validation ${validationId} failed:`, error);
            return {
                validationId,
                passed: false,
                score: 0,
                error: error.message,
                validationTime: Date.now() - startTime
            };
        }
    }

    /**
     * Perform comprehensive multi-dimensional validation
     */
    async performComprehensiveValidation(content, context) {
        const results = {};
        const weights = this.domainWeights[context.domain] || this.domainWeights['general-psychology'];

        // Validate each weighted criterion
        for (const [criterionName, weight] of Object.entries(weights)) {
            console.log(`[QualityValidator] Validating ${criterionName}`);

            try {
                const criterionResult = await this.validateCriterion(criterionName, content, context);
                results[criterionName] = {
                    ...criterionResult,
                    weight: weight,
                    contribution: criterionResult.score * weight
                };
            } catch (error) {
                console.warn(`[QualityValidator] Criterion ${criterionName} validation failed:`, error);
                results[criterionName] = {
                    passed: false,
                    score: 0,
                    weight: weight,
                    contribution: 0,
                    error: error.message
                };
            }
        }

        // Additional cross-cutting validations
        results.coherence = await this.validateCoherence(content, context);
        results.completeness = await this.validateCompleteness(content, context);
        results.accessibility = await this.validateAccessibility(content, context);

        return results;
    }

    /**
     * Validate individual criterion
     */
    async validateCriterion(criterionName, content, context) {
        const validationMethod = this.getValidationMethod(criterionName);

        if (validationMethod) {
            return await validationMethod.call(this, content, context);
        } else {
            // Generic validation based on rule sets
            return await this.genericCriterionValidation(criterionName, content, context);
        }
    }

    /**
     * Evidence quality validation
     */
    async validateEvidenceQuality(content, context) {
        console.log(`[QualityValidator] Validating evidence quality`);

        const evidence = this.extractEvidence(content);
        const score = {
            peerReviewed: 0,
            recency: 0,
            methodologicalRigor: 0,
            effectSize: 0,
            total: 0
        };

        // Check for peer-reviewed sources
        score.peerReviewed = this.assessPeerReviewedSources(evidence);

        // Check recency of research
        score.recency = this.assessResearchRecency(evidence);

        // Assess methodological rigor
        score.methodologicalRigor = this.assessMethodologicalRigor(evidence);

        // Check for effect size reporting
        score.effectSize = this.assessEffectSizeReporting(evidence);

        // Calculate total score
        score.total = (score.peerReviewed + score.recency + score.methodologicalRigor + score.effectSize) / 4;

        return {
            passed: score.total >= 0.75,
            score: score.total,
            details: score,
            evidence: evidence.length,
            feedback: this.generateEvidenceFeedback(score)
        };
    }

    /**
     * Safety assessment validation
     */
    async validateSafetyAssessment(content, context) {
        console.log(`[QualityValidator] Validating safety assessment`);

        const safetyElements = this.extractSafetyElements(content);
        const score = {
            contraindications: 0,
            riskFactors: 0,
            protocols: 0,
            adverseEffects: 0,
            supervision: 0,
            total: 0
        };

        // Check contraindications
        score.contraindications = this.assessContraindications(safetyElements);

        // Check risk factor assessment
        score.riskFactors = this.assessRiskFactors(safetyElements);

        // Check safety protocols
        score.protocols = this.assessSafetyProtocols(safetyElements);

        // Check adverse effects documentation
        score.adverseEffects = this.assessAdverseEffectsDocumentation(safetyElements);

        // Check supervision requirements
        score.supervision = this.assessSupervisionRequirements(safetyElements);

        score.total = (score.contraindications + score.riskFactors + score.protocols +
                      score.adverseEffects + score.supervision) / 5;

        return {
            passed: score.total >= 0.90,
            score: score.total,
            details: score,
            mandatory: true,
            feedback: this.generateSafetyFeedback(score),
            riskLevel: this.assessOverallRiskLevel(score)
        };
    }

    /**
     * Ethical compliance validation
     */
    async validateEthicalCompliance(content, context) {
        console.log(`[QualityValidator] Validating ethical compliance`);

        const ethicalElements = this.extractEthicalElements(content);
        const score = {
            informedConsent: 0,
            confidentiality: 0,
            boundaries: 0,
            culturalSensitivity: 0,
            doNoHarm: 0,
            total: 0
        };

        // Check informed consent procedures
        score.informedConsent = this.assessInformedConsent(ethicalElements);

        // Check confidentiality measures
        score.confidentiality = this.assessConfidentiality(ethicalElements);

        // Check professional boundaries
        score.boundaries = this.assessProfessionalBoundaries(ethicalElements);

        // Check cultural sensitivity
        score.culturalSensitivity = this.assessCulturalSensitivity(ethicalElements);

        // Check do-no-harm principle
        score.doNoHarm = this.assessDoNoHarm(ethicalElements);

        score.total = (score.informedConsent + score.confidentiality + score.boundaries +
                      score.culturalSensitivity + score.doNoHarm) / 5;

        return {
            passed: score.total >= 0.85,
            score: score.total,
            details: score,
            mandatory: true,
            feedback: this.generateEthicalFeedback(score),
            ethicalRisk: this.assessEthicalRisk(score)
        };
    }

    /**
     * Pedagogical soundness validation (for educational content)
     */
    async validatePedagogicalSoundness(content, context) {
        console.log(`[QualityValidator] Validating pedagogical soundness`);

        const pedagogicalElements = this.extractPedagogicalElements(content);
        const score = {
            learningObjectives: 0,
            scaffolding: 0,
            activeLearning: 0,
            feedback: 0,
            transfer: 0,
            total: 0
        };

        // Check learning objectives
        score.learningObjectives = this.assessLearningObjectives(pedagogicalElements);

        // Check scaffolding
        score.scaffolding = this.assessScaffolding(pedagogicalElements);

        // Check active learning elements
        score.activeLearning = this.assessActiveLearning(pedagogicalElements);

        // Check feedback mechanisms
        score.feedback = this.assessFeedbackMechanisms(pedagogicalElements);

        // Check transfer support
        score.transfer = this.assessTransferSupport(pedagogicalElements);

        score.total = (score.learningObjectives + score.scaffolding + score.activeLearning +
                      score.feedback + score.transfer) / 5;

        return {
            passed: score.total >= 0.80,
            score: score.total,
            details: score,
            feedback: this.generatePedagogicalFeedback(score),
            learningEffectiveness: this.assessLearningEffectiveness(score)
        };
    }

    /**
     * Clinical accuracy validation
     */
    async validateClinicalAccuracy(content, context) {
        console.log(`[QualityValidator] Validating clinical accuracy`);

        const clinicalElements = this.extractClinicalElements(content);
        const score = {
            diagnosticPrecision: 0,
            treatmentProtocols: 0,
            outcomeMeasures: 0,
            professionalStandards: 0,
            evidenceAlignment: 0,
            total: 0
        };

        // Check diagnostic precision
        score.diagnosticPrecision = this.assessDiagnosticPrecision(clinicalElements);

        // Check treatment protocols
        score.treatmentProtocols = this.assessTreatmentProtocols(clinicalElements);

        // Check outcome measures
        score.outcomeMeasures = this.assessOutcomeMeasures(clinicalElements);

        // Check professional standards alignment
        score.professionalStandards = this.assessProfessionalStandards(clinicalElements);

        // Check evidence alignment
        score.evidenceAlignment = this.assessEvidenceAlignment(clinicalElements);

        score.total = (score.diagnosticPrecision + score.treatmentProtocols + score.outcomeMeasures +
                      score.professionalStandards + score.evidenceAlignment) / 5;

        return {
            passed: score.total >= 0.85,
            score: score.total,
            details: score,
            feedback: this.generateClinicalFeedback(score),
            clinicalRisk: this.assessClinicalRisk(score)
        };
    }

    /**
     * Generic criterion validation
     */
    async genericCriterionValidation(criterionName, content, context) {
        // Simplified generic validation
        const contentString = JSON.stringify(content).toLowerCase();
        const criterionKeywords = this.getCriterionKeywords(criterionName);

        let score = 0.5; // Base score

        // Check for positive indicators
        const positiveCount = criterionKeywords.positive?.filter(keyword =>
            contentString.includes(keyword)
        ).length || 0;

        // Check for negative indicators
        const negativeCount = criterionKeywords.negative?.filter(keyword =>
            contentString.includes(keyword)
        ).length || 0;

        // Calculate score based on indicators
        score += (positiveCount * 0.1) - (negativeCount * 0.2);
        score = Math.max(0, Math.min(1, score));

        return {
            passed: score >= 0.7,
            score: score,
            details: {
                positiveIndicators: positiveCount,
                negativeIndicators: negativeCount,
                criterion: criterionName
            },
            feedback: `Generic validation for ${criterionName}: ${positiveCount} positive indicators, ${negativeCount} negative indicators`
        };
    }

    /**
     * Cross-cutting validations
     */
    async validateCoherence(content, context) {
        // Check logical flow and consistency across content
        const coherenceScore = this.assessContentCoherence(content);

        return {
            passed: coherenceScore >= 0.7,
            score: coherenceScore,
            details: {
                logicalFlow: this.assessLogicalFlow(content),
                consistency: this.assessConsistency(content),
                connectivity: this.assessConnectivity(content)
            }
        };
    }

    async validateCompleteness(content, context) {
        // Check if all required elements are present
        const requiredElements = this.getRequiredElements(context.contentType, context.domain);
        const presentElements = this.identifyPresentElements(content);

        const completenessScore = presentElements.length / requiredElements.length;

        return {
            passed: completenessScore >= 0.8,
            score: completenessScore,
            details: {
                required: requiredElements.length,
                present: presentElements.length,
                missing: requiredElements.filter(el => !presentElements.includes(el))
            }
        };
    }

    async validateAccessibility(content, context) {
        // Check accessibility and inclusivity
        const accessibilityScore = this.assessAccessibility(content);

        return {
            passed: accessibilityScore >= 0.7,
            score: accessibilityScore,
            details: {
                readability: this.assessReadability(content),
                culturalInclusion: this.assessCulturalInclusion(content),
                languageClarity: this.assessLanguageClarity(content)
            }
        };
    }

    /**
     * Helper methods for specific assessments
     */
    extractEvidence(content) {
        // Extract evidence references from content
        const evidence = [];

        // Look for references, citations, studies
        const contentStr = JSON.stringify(content);
        const referencePatterns = [
            /\b(study|research|trial|meta-analysis|review)\b/gi,
            /\b\d{4}\b.*?et al\./gi,
            /\bdoi:|pmid:|isbn:/gi
        ];

        referencePatterns.forEach(pattern => {
            const matches = contentStr.match(pattern) || [];
            evidence.push(...matches);
        });

        return evidence;
    }

    assessPeerReviewedSources(evidence) {
        // Simple heuristic for peer-reviewed source detection
        const peerReviewedIndicators = ['journal', 'published', 'peer-review', 'doi:', 'pmid:'];

        const evidenceStr = evidence.join(' ').toLowerCase();
        const indicatorCount = peerReviewedIndicators.filter(indicator =>
            evidenceStr.includes(indicator)
        ).length;

        return Math.min(1.0, indicatorCount / 3);
    }

    calculateOverallScore(validationResults, context) {
        const weights = this.domainWeights[context.domain] || this.domainWeights['general-psychology'];
        let totalScore = 0;
        let totalWeight = 0;

        Object.entries(validationResults).forEach(([criterion, result]) => {
            const weight = weights[criterion] || 0.1; // Small weight for non-domain criteria
            totalScore += result.score * weight;
            totalWeight += weight;
        });

        return totalWeight > 0 ? totalScore / totalWeight : 0;
    }

    checkMandatoryRequirements(validationResults) {
        const mandatoryChecks = ['safety-assessment', 'ethical-compliance'];

        return mandatoryChecks.every(check => {
            const result = validationResults[check];
            return !result || result.passed; // Pass if not present or if it passed
        });
    }

    generateRecommendations(validationResults, context) {
        const recommendations = [];

        Object.entries(validationResults).forEach(([criterion, result]) => {
            if (!result.passed && result.score < 0.7) {
                recommendations.push({
                    criterion,
                    priority: result.mandatory ? 'high' : 'medium',
                    issue: `${criterion} score (${result.score.toFixed(2)}) below threshold`,
                    suggestion: this.getImprovementSuggestion(criterion, result),
                    impact: this.assessImpact(criterion, result.score)
                });
            }
        });

        // Sort by priority and impact
        recommendations.sort((a, b) => {
            const priorityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
            return priorityOrder[b.priority] - priorityOrder[a.priority];
        });

        return recommendations;
    }

    generateValidationSummary(validationResults, overallScore, passed) {
        const passedCriteria = Object.values(validationResults).filter(r => r.passed).length;
        const totalCriteria = Object.keys(validationResults).length;
        const mandatoryIssues = Object.values(validationResults).filter(r => r.mandatory && !r.passed).length;

        return {
            status: passed ? 'PASSED' : 'FAILED',
            overallScore: overallScore.toFixed(2),
            criteriaSuccess: `${passedCriteria}/${totalCriteria}`,
            mandatoryIssues,
            topStrengths: this.identifyTopStrengths(validationResults),
            criticalIssues: this.identifyCriticalIssues(validationResults)
        };
    }

    /**
     * Utility methods
     */
    getValidationMethod(criterionName) {
        const methodMap = {
            'evidence-quality': this.validateEvidenceQuality,
            'safety-assessment': this.validateSafetyAssessment,
            'ethical-compliance': this.validateEthicalCompliance,
            'pedagogical-soundness': this.validatePedagogicalSoundness,
            'clinical-accuracy': this.validateClinicalAccuracy
        };

        return methodMap[criterionName];
    }

    inferContentType(content) {
        const contentStr = JSON.stringify(content).toLowerCase();

        if (contentStr.includes('assessment') || contentStr.includes('test')) return 'assessment';
        if (contentStr.includes('curriculum') || contentStr.includes('course')) return 'educational';
        if (contentStr.includes('therapy') || contentStr.includes('treatment')) return 'clinical';
        if (contentStr.includes('intervention') || contentStr.includes('protocol')) return 'intervention';

        return 'general';
    }

    generateValidationId() {
        return `val_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    }

    recordValidationMetrics(validationId, result) {
        this.validationHistory.push({
            id: validationId,
            timestamp: new Date().toISOString(),
            passed: result.passed,
            score: result.score,
            domain: result.domain,
            contentType: result.contentType
        });

        // Update performance metrics
        const totalValidations = this.performanceMetrics.totalValidations;
        const currentAverage = this.performanceMetrics.averageScore;

        this.performanceMetrics.averageScore =
            ((currentAverage * (totalValidations - 1)) + result.score) / totalValidations;

        this.performanceMetrics.failureRate =
            this.validationHistory.filter(v => !v.passed).length / this.validationHistory.length;

        // Keep only last 100 validations
        if (this.validationHistory.length > 100) {
            this.validationHistory.shift();
        }
    }

    /**
     * Get validator status and metrics
     */
    getStatus() {
        return {
            totalValidations: this.performanceMetrics.totalValidations,
            averageScore: this.performanceMetrics.averageScore.toFixed(2),
            failureRate: (this.performanceMetrics.failureRate * 100).toFixed(1) + '%',
            currentThreshold: this.config.threshold,
            domain: this.config.domain,
            strictMode: this.config.strictMode,
            recentValidations: this.validationHistory.slice(-5),
            availableDomains: Object.keys(this.domainWeights),
            validationCriteria: Object.keys(this.validationRules)
        };
    }
}

module.exports = QualityValidator;