/**
 * Usage Examples for Psychology Content Orchestrator
 * Demonstrates various ways to use the universal orchestrator agent
 */

const PsychologyContentOrchestrator = require('../core/orchestrator');

/**
 * Example 1: Basic Therapeutic Program Creation
 */
async function createTherapeuticProgram() {
    console.log('\n=== Example 1: Creating Therapeutic Program ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'clinical-psychology',
        integrationStrategy: 'clinical-protocols',
        qualityThreshold: 0.9,
        ragEnabled: true
    });

    const request = {
        type: 'therapeutic-program',
        description: 'Создать программу когнитивно-поведенческой терапии для лечения тревожных расстройств у взрослых',
        domain: 'clinical-psychology',
        targetAudience: 'adults-with-anxiety',
        objectives: [
            'Снижение уровня тревожности',
            'Развитие навыков совладания со стрессом',
            'Улучшение качества жизни',
            'Предотвращение рецидивов'
        ],
        parameters: {
            duration: '12-16 sessions',
            format: 'individual-therapy',
            evidenceLevel: 'high',
            culturalAdaptation: true
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Therapeutic program created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`⏱️ Completion Time: ${result.metrics.completionTime}ms`);
            console.log(`🤖 Agents Used: ${result.metrics.agentsUsed}`);
            console.log(`📝 Content Sections: ${Object.keys(result.content.sections).length}`);
        } else {
            console.log('❌ Failed to create therapeutic program:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating therapeutic program:', error);
        return null;
    }
}

/**
 * Example 2: Educational Assessment Tool Development
 */
async function createEducationalAssessment() {
    console.log('\n=== Example 2: Creating Educational Assessment Tool ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'educational-psychology',
        integrationStrategy: 'educational-curriculum',
        qualityThreshold: 0.85,
        ragEnabled: true
    });

    const request = {
        type: 'assessment-tool',
        description: 'Разработать инструмент оценки мотивации к обучению для студентов университета',
        domain: 'educational-psychology',
        targetAudience: 'university-students',
        objectives: [
            'Измерение внутренней мотивации',
            'Оценка академической самоэффективности',
            'Выявление факторов демотивации',
            'Планирование индивидуальной поддержки'
        ],
        parameters: {
            assessmentType: 'self-report-questionnaire',
            items: 40,
            scales: ['intrinsic-motivation', 'extrinsic-motivation', 'amotivation', 'self-efficacy'],
            validity: 'construct-validity-required',
            reliability: 'cronbach-alpha-0.80'
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Assessment tool created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`🎯 Assessment Framework: ${result.content.sections['assessment-framework']?.title}`);
            console.log(`📋 Validation Protocol: ${result.content.sections['quality-assurance']?.title}`);
        } else {
            console.log('❌ Failed to create assessment tool:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating assessment tool:', error);
        return null;
    }
}

/**
 * Example 3: Organizational Wellness Program
 */
async function createOrganizationalWellnessProgram() {
    console.log('\n=== Example 3: Creating Organizational Wellness Program ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'organizational-psychology',
        integrationStrategy: 'organizational-systems',
        qualityThreshold: 0.8,
        ragEnabled: true
    });

    const request = {
        type: 'comprehensive-program',
        description: 'Создать комплексную программу психологического благополучия сотрудников для IT-компании',
        domain: 'organizational-psychology',
        targetAudience: 'tech-professionals',
        objectives: [
            'Снижение профессионального выгорания',
            'Улучшение work-life balance',
            'Повышение командной эффективности',
            'Развитие стрессоустойчивости',
            'Создание поддерживающей культуры'
        ],
        parameters: {
            organizationSize: '500-1000 employees',
            industry: 'technology',
            implementationPhases: 4,
            duration: '12-months',
            measurementStrategy: 'quarterly-assessments',
            stakeholders: ['hr', 'management', 'employees', 'unions']
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Organizational wellness program created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`🏢 Implementation Guide: ${result.content.sections['implementation-guide']?.title}`);
            console.log(`📈 Business Alignment: Strong organizational fit`);
        } else {
            console.log('❌ Failed to create wellness program:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating wellness program:', error);
        return null;
    }
}

/**
 * Example 4: Research Methodology Framework
 */
async function createResearchFramework() {
    console.log('\n=== Example 4: Creating Research Methodology Framework ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'general-psychology',
        integrationStrategy: 'standard',
        qualityThreshold: 0.9,
        ragEnabled: true
    });

    const request = {
        type: 'research-methodology',
        description: 'Разработать методологическую рамку для исследования эффективности цифровых психологических интервенций',
        domain: 'general-psychology',
        targetAudience: 'researchers-clinicians',
        objectives: [
            'Стандартизация исследовательских процедур',
            'Обеспечение методологической строгости',
            'Сравнимость результатов исследований',
            'Этическое соответствие',
            'Практическая применимость'
        ],
        parameters: {
            researchDesign: 'randomized-controlled-trial',
            populationFocus: 'digital-interventions',
            outcomeMeasures: 'validated-instruments',
            statisticalPower: '80-percent',
            effectSize: 'medium-to-large',
            followUpPeriod: '6-months'
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Research framework created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`🔬 Theoretical Foundation: ${result.content.sections['theoretical-foundation']?.title}`);
            console.log(`📋 Quality Assurance: ${result.content.sections['quality-assurance']?.title}`);
        } else {
            console.log('❌ Failed to create research framework:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating research framework:', error);
        return null;
    }
}

/**
 * Example 5: Custom Domain Configuration
 */
async function demonstrateCustomDomain() {
    console.log('\n=== Example 5: Custom Domain Configuration ===');

    // Create orchestrator with custom domain settings
    const customDomainSettings = {
        'sports-psychology': {
            name: 'Sports Psychology',
            requirements: [
                'performance-focus',
                'athlete-specificity',
                'sport-context',
                'mental-skills-training'
            ],
            validation: [
                'performance-validity',
                'sport-relevance',
                'practical-application'
            ],
            approaches: [
                'cognitive-behavioral',
                'mindfulness-based',
                'goal-setting',
                'visualization'
            ],
            integrationStrategy: 'performance-optimization',
            qualityThreshold: 0.8
        }
    };

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'sports-psychology',
        domainSettings: customDomainSettings,
        integrationStrategy: 'performance-optimization',
        qualityThreshold: 0.8,
        ragEnabled: true
    });

    const request = {
        type: 'technique-library',
        description: 'Создать библиотеку ментальных техник для профессиональных теннисистов',
        domain: 'sports-psychology',
        targetAudience: 'professional-tennis-players',
        objectives: [
            'Улучшение концентрации во время матча',
            'Управление предсоревновательной тревожностью',
            'Быстрое восстановление после ошибок',
            'Повышение уверенности в себе'
        ],
        parameters: {
            sportSpecific: 'tennis',
            level: 'professional',
            techniques: ['visualization', 'self-talk', 'breathing', 'focus-cues'],
            practiceIntegration: true,
            competitionReady: true
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Sports psychology techniques created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`🎾 Sport-Specific Content: Tennis-focused techniques`);
            console.log(`🏆 Performance Orientation: Competition-ready protocols`);
        } else {
            console.log('❌ Failed to create sports psychology content:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating sports psychology content:', error);
        return null;
    }
}

/**
 * Example 6: Multi-Domain Integration
 */
async function demonstrateMultiDomainIntegration() {
    console.log('\n=== Example 6: Multi-Domain Integration ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'general-psychology',
        integrationStrategy: 'holistic-wellbeing',
        qualityThreshold: 0.85,
        ragEnabled: true
    });

    const request = {
        type: 'comprehensive-program',
        description: 'Создать интегрированную программу психологического благополучия, объединяющую клинические, образовательные и организационные подходы',
        domain: 'general-psychology',
        targetAudience: 'healthcare-workers',
        objectives: [
            'Профилактика профессионального выгорания',
            'Развитие эмоциональной устойчивости',
            'Обучение техникам самопомощи',
            'Создание поддерживающего сообщества',
            'Улучшение качества пациентоориентированной помощи'
        ],
        parameters: {
            multiDomain: true,
            clinicalComponent: 'stress-management-therapy',
            educationalComponent: 'resilience-training',
            organizationalComponent: 'workplace-wellness',
            healthComponent: 'self-care-protocols',
            integrationLevel: 'high',
            customization: 'role-specific'
        }
    };

    try {
        const result = await orchestrator.createContent(request);

        if (result.success) {
            console.log('✅ Multi-domain program created successfully!');
            console.log(`📊 Quality Score: ${result.quality.score.toFixed(2)}`);
            console.log(`🔄 Integration Features: ${Object.keys(result.content.integrationFeatures || {}).length}`);
            console.log(`🌐 Cross-Domain Coherence: Holistic approach implemented`);
        } else {
            console.log('❌ Failed to create multi-domain program:', result.error);
        }

        return result;

    } catch (error) {
        console.error('💥 Error creating multi-domain program:', error);
        return null;
    }
}

/**
 * Example 7: Real-time Status Monitoring
 */
async function demonstrateStatusMonitoring() {
    console.log('\n=== Example 7: Real-time Status Monitoring ===');

    const orchestrator = new PsychologyContentOrchestrator({
        domain: 'clinical-psychology',
        ragEnabled: true
    });

    // Start a content creation process
    const request = {
        type: 'assessment-tool',
        description: 'Краткий инструмент скрининга депрессии для первичного звена здравоохранения',
        domain: 'clinical-psychology',
        targetAudience: 'primary-care-patients',
        objectives: ['early-detection', 'risk-assessment', 'referral-guidance']
    };

    console.log('🚀 Starting content creation...');

    // Monitor status during creation
    const statusInterval = setInterval(() => {
        const status = orchestrator.getStatus();
        console.log(`⏳ Active workflows: ${status.activeWorkflows}`);
        console.log(`📈 Success rate: ${(status.successRate * 100).toFixed(1)}%`);
        console.log(`⭐ Average quality: ${status.averageQuality.toFixed(2)}`);
    }, 2000);

    try {
        const result = await orchestrator.createContent(request);

        clearInterval(statusInterval);

        if (result.success) {
            console.log('\n✅ Content creation completed!');

            // Final status
            const finalStatus = orchestrator.getStatus();
            console.log('\n📊 Final Statistics:');
            console.log(`   Total processed: ${finalStatus.totalProcessed}`);
            console.log(`   Success rate: ${(finalStatus.successRate * 100).toFixed(1)}%`);
            console.log(`   Average quality: ${finalStatus.averageQuality.toFixed(2)}`);
            console.log(`   Average completion time: ${finalStatus.averageCompletionTime.toFixed(0)}ms`);
        }

        return result;

    } catch (error) {
        clearInterval(statusInterval);
        console.error('💥 Error during monitored creation:', error);
        return null;
    }
}

/**
 * Main execution function to run all examples
 */
async function runAllExamples() {
    console.log('🎭 Psychology Content Orchestrator - Usage Examples');
    console.log('='.repeat(60));

    const examples = [
        createTherapeuticProgram,
        createEducationalAssessment,
        createOrganizationalWellnessProgram,
        createResearchFramework,
        demonstrateCustomDomain,
        demonstrateMultiDomainIntegration,
        demonstrateStatusMonitoring
    ];

    const results = [];

    for (const example of examples) {
        try {
            const result = await example();
            results.push(result);

            // Wait between examples
            await new Promise(resolve => setTimeout(resolve, 1000));

        } catch (error) {
            console.error(`💥 Example failed:`, error);
            results.push(null);
        }
    }

    console.log('\n🏁 All examples completed!');
    console.log(`✅ Successful: ${results.filter(r => r?.success).length}/${results.length}`);
    console.log(`❌ Failed: ${results.filter(r => !r?.success).length}/${results.length}`);

    return results;
}

// Export examples for individual use
module.exports = {
    createTherapeuticProgram,
    createEducationalAssessment,
    createOrganizationalWellnessProgram,
    createResearchFramework,
    demonstrateCustomDomain,
    demonstrateMultiDomainIntegration,
    demonstrateStatusMonitoring,
    runAllExamples
};

// Run examples if this file is executed directly
if (require.main === module) {
    runAllExamples().catch(console.error);
}