"""
Portfolio Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации портфолио сайтов.
Фокус на визуальной производительности, быстрой загрузке изображений и анимаций.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class PortfolioPerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для портфолио сайтов."""

    # Основные настройки
    domain_type: str = "portfolio"
    project_type: str = "showcase"
    framework: str = "next.js"

    # Performance специфичные настройки
    performance_type: str = "visual"
    optimization_strategy: str = "user_experience"

    # Целевые метрики для портфолио
    target_metrics: Dict[str, Any] = field(default_factory=lambda: {
        "first_contentful_paint": 1200,  # ms - быстрее для первого впечатления
        "largest_contentful_paint": 2000,  # ms - быстрая загрузка hero секции
        "cumulative_layout_shift": 0.05,  # очень низкий CLS для визуальной стабильности
        "first_input_delay": 50,  # ms - отзывчивое взаимодействие
        "total_blocking_time": 150,  # ms - плавные анимации
        "image_load_time": 800,  # ms - быстрая загрузка изображений
        "animation_fps": 60,  # плавные анимации
        "lighthouse_score": 95  # высокий балл для профессионального вида
    })

    # Portfolio-специфичные настройки
    enable_image_gallery_optimization: bool = True
    enable_smooth_animations: bool = True
    enable_progressive_image_loading: bool = True
    enable_video_optimization: bool = True
    enable_critical_hero_section: bool = True

    def __post_init__(self):
        super().__post_init__()

        # Portfolio knowledge tags
        self.knowledge_tags.extend([
            "portfolio-performance", "visual-optimization", "image-gallery",
            "animation-performance", "hero-section", "showcase-sites"
        ])

    def get_portfolio_performance_config(self) -> Dict[str, Any]:
        """Специфичная конфигурация для портфолио производительности."""
        return {
            "visual_optimization": {
                "hero_section": {
                    "critical_css_inline": self.enable_critical_hero_section,
                    "above_fold_priority": True,
                    "hero_image_preload": True,
                    "background_video_optimization": self.enable_video_optimization
                },
                "image_gallery": {
                    "progressive_loading": self.enable_progressive_image_loading,
                    "lazy_loading_threshold": "200px",
                    "image_format_optimization": True,
                    "responsive_images": True,
                    "placeholder_blur": True
                },
                "animations": {
                    "gpu_acceleration": self.enable_smooth_animations,
                    "will_change_optimization": True,
                    "intersection_observer": True,
                    "reduced_motion_support": True
                }
            },
            "content_optimization": {
                "typography": {
                    "font_display_swap": True,
                    "font_preload": True,
                    "variable_fonts": True,
                    "font_subset": True
                },
                "media": {
                    "video_lazy_loading": self.enable_video_optimization,
                    "webp_avif_support": True,
                    "responsive_video": True,
                    "poster_optimization": True
                }
            },
            "interaction": {
                "smooth_scrolling": {
                    "css_scroll_behavior": True,
                    "momentum_scrolling": True,
                    "scroll_snap": True
                },
                "navigation": {
                    "instant_navigation": True,
                    "prefetch_on_hover": True,
                    "back_button_cache": True
                }
            },
            "seo_performance": {
                "structured_data": True,
                "open_graph_optimization": True,
                "meta_optimization": True,
                "sitemap_generation": True
            }
        }

    def get_portfolio_optimization_techniques(self) -> List[str]:
        """Список техник оптимизации для портфолио."""
        return [
            "hero_section_optimization",
            "progressive_image_enhancement",
            "gallery_lazy_loading",
            "animation_gpu_acceleration",
            "critical_css_extraction",
            "font_optimization",
            "video_compression",
            "blur_placeholder_generation",
            "intersection_observer_implementation",
            "smooth_scroll_polyfill",
            "reduced_motion_queries",
            "portfolio_seo_optimization"
        ]

    def get_visual_performance_budget(self) -> Dict[str, Dict[str, float]]:
        """Performance budget для портфолио сайтов."""
        return {
            "visual_metrics": {
                "hero_image_size": 150,  # KB - оптимизированное hero изображение
                "gallery_image_size": 80,  # KB - размер изображений в галерее
                "total_images_above_fold": 3,  # количество изображений выше fold
                "animation_frame_budget": 16.67,  # ms для 60fps
                "font_load_time": 100  # ms максимальное время загрузки шрифтов
            },
            "content_budget": {
                "hero_section_html": 10,  # KB
                "critical_css": 15,  # KB
                "above_fold_js": 25,  # KB
                "total_fonts": 100,  # KB для всех шрифтов
                "video_poster": 50  # KB для постера видео
            },
            "interaction_budget": {
                "scroll_response": 16,  # ms максимальная задержка скролла
                "hover_response": 8,  # ms задержка hover эффектов
                "click_response": 100,  # ms время отклика на клик
                "animation_duration": 300  # ms максимальная длительность анимации
            }
        }

    def get_portfolio_assets_strategy(self) -> Dict[str, Any]:
        """Стратегия загрузки ресурсов для портфолио."""
        return {
            "critical_path": {
                "inline_critical_css": True,
                "preload_hero_image": True,
                "preload_primary_font": True,
                "defer_non_critical_js": True
            },
            "progressive_enhancement": {
                "base_experience": "fast_text_content",
                "enhanced_experience": "images_and_animations",
                "premium_experience": "videos_and_interactions"
            },
            "loading_priorities": {
                "hero_content": "high",
                "navigation": "high",
                "about_section": "medium",
                "portfolio_gallery": "medium",
                "contact_form": "low",
                "footer": "low"
            }
        }


# Пример использования
def get_portfolio_performance_dependencies() -> PortfolioPerformanceDependencies:
    """Создать конфигурацию для портфолио сайта."""
    return PortfolioPerformanceDependencies(
        project_path="/portfolio/site",
        project_name="Creative Portfolio",
        domain_type="portfolio",
        project_type="showcase",
        framework="next.js",
        performance_type="visual",
        optimization_strategy="user_experience",
        enable_image_gallery_optimization=True,
        enable_smooth_animations=True,
        enable_progressive_image_loading=True
    )


# Пример использования в Portfolio сайте
PORTFOLIO_PERFORMANCE_EXAMPLES = {
    "next_config_portfolio": """
// next.config.js - Portfolio Performance Optimization
const nextConfig = {
  // Optimized for visual content
  swcMinify: true,

  // Image optimization for portfolio
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384, 512],
    minimumCacheTTL: 31536000, // 1 year cache for portfolio images
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Performance optimizations for visual content
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
    optimizePackageImports: ['framer-motion', 'lottie-react'],
  },

  // Headers for optimal caching
  async headers() {
    return [
      {
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/videos/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },

  // Webpack optimization for animations
  webpack: (config) => {
    config.optimization.splitChunks.chunks = 'all';
    config.optimization.splitChunks.cacheGroups = {
      ...config.optimization.splitChunks.cacheGroups,
      animations: {
        name: 'animations',
        test: /[\\/]node_modules[\\/](framer-motion|lottie-react|gsap)[\\/]/,
        chunks: 'all',
        priority: 20,
      },
    };
    return config;
  },
};

module.exports = nextConfig;
""",

    "hero_section_component": """
// Performance-optimized Hero section for portfolio
import { memo, useState, useEffect } from 'react';
import Image from 'next/image';
import { motion, useReducedMotion } from 'framer-motion';

const OptimizedHeroSection = memo(({ portfolioConfig }) => {
  const shouldReduceMotion = useReducedMotion();
  const [imageLoaded, setImageLoaded] = useState(false);
  const performanceConfig = portfolioConfig.get_portfolio_performance_config();

  // Animation variants with reduced motion support
  const heroVariants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: shouldReduceMotion ? 0.1 : 0.8,
        ease: "easeOut"
      }
    }
  };

  // Preload critical resources
  useEffect(() => {
    if (performanceConfig.visual_optimization.hero_section.hero_image_preload) {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = '/hero-image-optimized.avif';
      document.head.appendChild(link);
    }
  }, [performanceConfig]);

  return (
    <section className="hero-section" style={{ minHeight: '100vh' }}>
      {/* Critical CSS inlined for hero section */}
      <style jsx>{`
        .hero-section {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          will-change: transform;
        }
        .hero-content {
          text-align: center;
          z-index: 2;
          max-width: 800px;
          padding: 2rem;
        }
        .hero-title {
          font-size: clamp(2rem, 5vw, 4rem);
          font-weight: 700;
          margin-bottom: 1.5rem;
          line-height: 1.2;
          color: white;
        }
        .hero-image-container {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
          opacity: ${imageLoaded ? 0.2 : 0};
          transition: opacity 0.5s ease;
        }
      `}</style>

      {/* Optimized background image */}
      <div className="hero-image-container">
        <Image
          src="/hero-image-optimized.avif"
          alt="Portfolio hero background"
          fill
          style={{ objectFit: 'cover' }}
          priority
          quality={85}
          placeholder="blur"
          blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
          onLoad={() => setImageLoaded(true)}
          sizes="100vw"
        />
      </div>

      {/* Hero content with optimized animations */}
      <motion.div
        className="hero-content"
        variants={heroVariants}
        initial="hidden"
        animate="visible"
      >
        <h1 className="hero-title">
          Creative Portfolio
        </h1>
        <motion.p
          style={{
            fontSize: '1.25rem',
            marginBottom: '2rem',
            color: 'rgba(255, 255, 255, 0.9)'
          }}
          variants={heroVariants}
          transition={{ delay: shouldReduceMotion ? 0 : 0.2 }}
        >
          Showcasing exceptional design and development
        </motion.p>

        {/* CTA with hover optimization */}
        <motion.button
          className="hero-cta"
          variants={heroVariants}
          transition={{ delay: shouldReduceMotion ? 0 : 0.4 }}
          whileHover={shouldReduceMotion ? {} : { scale: 1.05 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.95 }}
          style={{
            padding: '1rem 2rem',
            fontSize: '1.1rem',
            border: '2px solid white',
            backgroundColor: 'transparent',
            color: 'white',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease'
          }}
        >
          View My Work
        </motion.button>
      </motion.div>
    </section>
  );
});

OptimizedHeroSection.displayName = 'OptimizedHeroSection';

export default OptimizedHeroSection;
""",

    "portfolio_gallery": """
// Performance-optimized Portfolio Gallery
import { memo, useState, useCallback, useMemo } from 'react';
import Image from 'next/image';
import { motion, AnimatePresence } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const PortfolioGallery = memo(({ projects, portfolioConfig }) => {
  const [selectedProject, setSelectedProject] = useState(null);
  const performanceConfig = portfolioConfig.get_portfolio_performance_config();

  // Virtualization for large portfolios
  const visibleProjects = useMemo(() =>
    projects.slice(0, 12) // Initially show 12 projects
  , [projects]);

  return (
    <section className="portfolio-gallery">
      <div className="gallery-grid">
        {visibleProjects.map((project, index) => (
          <ProjectCard
            key={project.id}
            project={project}
            index={index}
            onSelect={setSelectedProject}
            performanceConfig={performanceConfig}
          />
        ))}
      </div>

      {/* Modal with lazy loading */}
      <AnimatePresence>
        {selectedProject && (
          <ProjectModal
            project={selectedProject}
            onClose={() => setSelectedProject(null)}
            performanceConfig={performanceConfig}
          />
        )}
      </AnimatePresence>
    </section>
  );
});

const ProjectCard = memo(({ project, index, onSelect, performanceConfig }) => {
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true,
    rootMargin: performanceConfig.visual_optimization.image_gallery.lazy_loading_threshold
  });

  const handleClick = useCallback(() => {
    onSelect(project);
  }, [project, onSelect]);

  return (
    <motion.div
      ref={ref}
      className="project-card"
      onClick={handleClick}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ delay: index * 0.1, duration: 0.6 }}
      whileHover={{ scale: 1.03 }}
      style={{
        cursor: 'pointer',
        borderRadius: '12px',
        overflow: 'hidden',
        backgroundColor: 'white',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
        transition: 'box-shadow 0.3s ease'
      }}
    >
      {inView && (
        <>
          <div style={{ position: 'relative', aspectRatio: '16/10' }}>
            <Image
              src={project.thumbnail}
              alt={project.title}
              fill
              style={{ objectFit: 'cover' }}
              placeholder="blur"
              blurDataURL={project.blurDataURL}
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              quality={performanceConfig.visual_optimization.image_gallery.image_format_optimization ? 85 : 75}
            />
          </div>
          <div style={{ padding: '1.5rem' }}>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.25rem' }}>
              {project.title}
            </h3>
            <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
              {project.description}
            </p>
          </div>
        </>
      )}
    </motion.div>
  );
});

const ProjectModal = memo(({ project, onClose, performanceConfig }) => {
  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000
      }}
    >
      <motion.div
        className="modal-content"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: 'white',
          borderRadius: '12px',
          maxWidth: '90vw',
          maxHeight: '90vh',
          overflow: 'auto'
        }}
      >
        {/* Modal content with optimized loading */}
        <div style={{ position: 'relative', aspectRatio: '16/10' }}>
          <Image
            src={project.fullImage}
            alt={project.title}
            fill
            style={{ objectFit: 'cover' }}
            priority
            quality={90}
            sizes="90vw"
          />
        </div>
        <div style={{ padding: '2rem' }}>
          <h2>{project.title}</h2>
          <p>{project.fullDescription}</p>
          <div style={{ marginTop: '1rem' }}>
            {project.technologies.map(tech => (
              <span
                key={tech}
                style={{
                  display: 'inline-block',
                  padding: '0.25rem 0.75rem',
                  margin: '0.25rem',
                  backgroundColor: '#f0f0f0',
                  borderRadius: '20px',
                  fontSize: '0.8rem'
                }}
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
});

PortfolioGallery.displayName = 'PortfolioGallery';
ProjectCard.displayName = 'ProjectCard';
ProjectModal.displayName = 'ProjectModal';

export default PortfolioGallery;
"""
}