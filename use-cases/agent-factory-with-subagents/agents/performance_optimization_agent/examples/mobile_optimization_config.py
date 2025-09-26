"""
Mobile Application Performance конфигурация для Performance Optimization Agent.

Этот файл демонстрирует настройку агента для оптимизации мобильных приложений.
Включает настройки для React Native, Flutter, и нативных iOS/Android приложений.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from ..dependencies import PerformanceOptimizationDependencies


@dataclass
class MobilePerformanceDependencies(PerformanceOptimizationDependencies):
    """Конфигурация для мобильных приложений."""

    # Основные настройки
    domain_type: str = "mobile"
    project_type: str = "react_native"
    framework: str = "react_native"

    # Performance специфичные настройки
    performance_type: str = "mobile"
    optimization_strategy: str = "memory"

    # Целевые метрики для мобильных приложений
    target_metrics: Dict[str, Any] = field(default_factory=lambda: {
        "app_start_time": 2000,     # ms - cold start
        "warm_start_time": 500,     # ms - warm start
        "memory_usage": 150,        # MB
        "battery_usage": 5,         # % per hour
        "cpu_usage": 0.3,           # 30%
        "network_efficiency": 0.9,  # 90%
        "frame_rate": 60,           # FPS
        "js_bundle_size": 10,       # MB for React Native
        "image_cache_size": 50,     # MB
        "crash_rate": 0.001         # 0.1%
    })

    # Mobile специфичные настройки
    enable_code_push: bool = True
    enable_lazy_initialization: bool = True
    enable_image_caching: bool = True
    enable_offline_support: bool = True
    enable_background_optimization: bool = True

    # Platform настройки
    target_platforms: List[str] = field(default_factory=lambda: ["ios", "android"])
    enable_native_optimization: bool = True
    enable_bundle_splitting: bool = True

    def __post_init__(self):
        super().__post_init__()

        # Mobile performance knowledge tags
        self.knowledge_tags.extend([
            "mobile-performance", "react-native", "flutter", "ios", "android",
            "battery-optimization", "memory-management", "app-startup"
        ])

    def get_mobile_performance_config(self) -> Dict[str, Any]:
        """Специфичная конфигурация для мобильной производительности."""
        return {
            "startup_optimization": {
                "lazy_initialization": self.enable_lazy_initialization,
                "splash_screen_optimization": True,
                "preload_critical_data": True,
                "defer_non_critical": True
            },
            "memory_management": {
                "image_caching": self.enable_image_caching,
                "memory_warnings": True,
                "garbage_collection": True,
                "memory_profiling": True
            },
            "battery_optimization": {
                "background_optimization": self.enable_background_optimization,
                "location_optimization": True,
                "network_batching": True,
                "cpu_throttling": True
            },
            "rendering": {
                "frame_rate_optimization": True,
                "ui_thread_optimization": True,
                "layout_optimization": True,
                "animation_optimization": True
            },
            "networking": {
                "request_batching": True,
                "offline_support": self.enable_offline_support,
                "cache_management": True,
                "compression": True
            },
            "bundle_optimization": {
                "code_splitting": self.enable_bundle_splitting,
                "dead_code_elimination": True,
                "minification": True,
                "tree_shaking": True
            }
        }

    def get_platform_specific_config(self) -> Dict[str, Dict[str, Any]]:
        """Конфигурация для конкретных платформ."""
        return {
            "ios": {
                "app_thinning": True,
                "bitcode": True,
                "metal_rendering": True,
                "background_app_refresh": False,
                "precompiled_headers": True,
                "link_time_optimization": True
            },
            "android": {
                "proguard": True,
                "r8_optimization": True,
                "app_bundle": True,
                "vector_drawables": True,
                "background_limits": True,
                "adaptive_icons": True
            },
            "react_native": {
                "hermes_engine": True,
                "flipper_enabled": False,  # Only in development
                "metro_bundler_optimization": True,
                "native_modules_optimization": True
            },
            "flutter": {
                "aot_compilation": True,
                "tree_shaking": True,
                "obfuscation": True,
                "split_debug_info": True
            }
        }

    def get_battery_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация оптимизации батареи."""
        return {
            "background_tasks": {
                "limit_background_execution": True,
                "efficient_background_sync": True,
                "background_app_refresh": False,
                "push_notifications_only": True
            },
            "location_services": {
                "use_significant_location_changes": True,
                "reduce_location_accuracy": True,
                "stop_location_updates": True,
                "geofencing_optimization": True
            },
            "networking": {
                "batch_network_requests": True,
                "reduce_polling_frequency": True,
                "use_push_instead_of_pull": True,
                "compress_data": True
            },
            "ui_optimization": {
                "reduce_animation_fps": True,
                "optimize_scrolling": True,
                "lazy_load_images": True,
                "reduce_transparency": True
            }
        }

    def get_memory_optimization_config(self) -> Dict[str, Any]:
        """Конфигурация оптимизации памяти."""
        return {
            "image_management": {
                "image_caching": self.enable_image_caching,
                "image_compression": True,
                "lazy_image_loading": True,
                "image_format_optimization": True,
                "memory_cache_limit": "50MB"
            },
            "data_management": {
                "efficient_data_structures": True,
                "object_pooling": True,
                "weak_references": True,
                "memory_leaks_detection": True
            },
            "garbage_collection": {
                "gc_optimization": True,
                "avoid_retain_cycles": True,
                "autoreleasepool": True,  # iOS specific
                "memory_warnings_handling": True
            }
        }


# Пример использования
def get_mobile_performance_dependencies() -> MobilePerformanceDependencies:
    """Создать конфигурацию для мобильного приложения."""
    return MobilePerformanceDependencies(
        project_path="/mobile/app",
        project_name="High Performance Mobile App",
        domain_type="mobile",
        project_type="react_native",
        framework="react_native",
        performance_type="mobile",
        optimization_strategy="memory",
        enable_lazy_initialization=True,
        enable_image_caching=True,
        enable_background_optimization=True
    )


# Примеры оптимизированного мобильного кода
MOBILE_PERFORMANCE_EXAMPLES = {
    "react_native_optimized": """
// React Native Performance Optimizations
import React, { memo, useMemo, useCallback, useRef } from 'react';
import {
  View,
  Text,
  Image,
  FlatList,
  InteractionManager,
  LayoutAnimation,
  Platform,
  UIManager
} from 'react-native';
import FastImage from 'react-native-fast-image';
import { useQuery } from '@tanstack/react-query';

// Enable LayoutAnimation on Android
if (Platform.OS === 'android') {
  if (UIManager.setLayoutAnimationEnabledExperimental) {
    UIManager.setLayoutAnimationEnabledExperimental(true);
  }
}

// Memoized component for list items
const OptimizedListItem = memo(({ item, onPress, config }) => {
  const performanceConfig = config.get_mobile_performance_config();

  const handlePress = useCallback(() => {
    onPress(item.id);
  }, [item.id, onPress]);

  return (
    <View style={styles.itemContainer}>
      {/* Optimized image loading */}
      {performanceConfig.memory_management.image_caching && (
        <FastImage
          source={{ uri: item.image }}
          style={styles.image}
          resizeMode={FastImage.resizeMode.cover}
          priority={FastImage.priority.normal}
          cache={FastImage.cacheControl.immutable}
        />
      )}

      <View style={styles.textContainer}>
        <Text style={styles.title} numberOfLines={2}>
          {item.title}
        </Text>
        <Text style={styles.description} numberOfLines={3}>
          {item.description}
        </Text>
      </View>

      <TouchableOpacity
        style={styles.button}
        onPress={handlePress}
        activeOpacity={0.7}
      >
        <Text style={styles.buttonText}>View</Text>
      </TouchableOpacity>
    </View>
  );
});

// Main component with performance optimizations
const OptimizedProductList = ({ config }) => {
  const flatListRef = useRef(null);

  // Lazy loading with React Query
  const { data: products, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000,   // 10 minutes
  });

  // Memoized render item function
  const renderItem = useCallback(({ item }) => (
    <OptimizedListItem
      item={item}
      onPress={handleItemPress}
      config={config}
    />
  ), [config]);

  // Memoized key extractor
  const keyExtractor = useCallback((item) => item.id.toString(), []);

  // Optimized item press handler
  const handleItemPress = useCallback((itemId) => {
    InteractionManager.runAfterInteractions(() => {
      // Defer navigation until interactions are complete
      navigation.navigate('ProductDetail', { id: itemId });
    });
  }, [navigation]);

  // Memoized list configuration
  const listConfig = useMemo(() => ({
    initialNumToRender: 10,
    maxToRenderPerBatch: 5,
    windowSize: 10,
    removeClippedSubviews: true,
    getItemLayout: (data, index) => ({
      length: 120,
      offset: 120 * index,
      index,
    }),
  }), []);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <FlatList
      ref={flatListRef}
      data={products}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      {...listConfig}
      onEndReachedThreshold={0.5}
      onEndReached={loadMoreProducts}
    />
  );
};

export default OptimizedProductList;
""",

    "flutter_optimized": """
// Flutter Performance Optimizations
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';

class OptimizedProductList extends StatefulWidget {
  final MobilePerformanceConfig config;

  const OptimizedProductList({Key? key, required this.config}) : super(key: key);

  @override
  _OptimizedProductListState createState() => _OptimizedProductListState();
}

class _OptimizedProductListState extends State<OptimizedProductList>
    with AutomaticKeepAliveClientMixin {

  late ScrollController _scrollController;
  final List<Product> _products = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    _loadInitialProducts();
  }

  @override
  bool get wantKeepAlive => true;

  Future<void> _loadInitialProducts() async {
    setState(() => _isLoading = true);

    try {
      final products = await ProductService.fetchProducts(limit: 20);
      setState(() {
        _products.addAll(products);
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    super.build(context);

    return Scaffold(
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              controller: _scrollController,
              itemCount: _products.length,
              // Performance optimization: specify item extent
              itemExtent: 120.0,
              // Use RepaintBoundary to isolate repaints
              itemBuilder: (context, index) => RepaintBoundary(
                child: OptimizedProductTile(
                  product: _products[index],
                  config: widget.config,
                ),
              ),
            ),
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}

class OptimizedProductTile extends StatelessWidget {
  final Product product;
  final MobilePerformanceConfig config;

  const OptimizedProductTile({
    Key? key,
    required this.product,
    required this.config,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: () => _handleTap(context),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              // Optimized image widget
              _buildOptimizedImage(),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      product.name,
                      style: Theme.of(context).textTheme.titleMedium,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      product.description,
                      style: Theme.of(context).textTheme.bodySmall,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildOptimizedImage() {
    if (config.memoryManagement.imageCaching) {
      return CachedNetworkImage(
        imageUrl: product.imageUrl,
        width: 80,
        height: 80,
        fit: BoxFit.cover,
        memCacheWidth: 160, // 2x for high DPI
        memCacheHeight: 160,
        placeholder: (context, url) => Container(
          width: 80,
          height: 80,
          color: Colors.grey[300],
          child: const Icon(Icons.image),
        ),
        errorWidget: (context, url, error) => Container(
          width: 80,
          height: 80,
          color: Colors.grey[300],
          child: const Icon(Icons.error),
        ),
      );
    }

    return Image.network(
      product.imageUrl,
      width: 80,
      height: 80,
      fit: BoxFit.cover,
      loadingBuilder: (context, child, progress) {
        if (progress == null) return child;
        return Container(
          width: 80,
          height: 80,
          color: Colors.grey[300],
          child: const CircularProgressIndicator(),
        );
      },
    );
  }

  void _handleTap(BuildContext context) {
    // Use haptic feedback for better UX
    HapticFeedback.lightImpact();

    Navigator.pushNamed(
      context,
      '/product-detail',
      arguments: product.id,
    );
  }
}

// Memory optimization utility
class MemoryOptimizer {
  static void optimizeImageCache() {
    // Clear image cache when memory is low
    PaintingBinding.instance.imageCache.clear();
    PaintingBinding.instance.imageCache.clearLiveImages();
  }

  static void handleMemoryWarning() {
    // Handle low memory situations
    optimizeImageCache();

    // Clear unnecessary caches
    Provider.debugCheckInvalidValueType = null;
  }
}
""",

    "ios_swift_optimized": """
// iOS Swift Performance Optimizations
import UIKit
import Foundation

class OptimizedProductViewController: UIViewController {

    @IBOutlet weak var collectionView: UICollectionView!

    private var products: [Product] = []
    private let imageCache = NSCache<NSString, UIImage>()
    private var config: MobilePerformanceConfig

    // Prefetching for performance
    private let prefetchDataSource = ProductPrefetchDataSource()

    init(config: MobilePerformanceConfig) {
        self.config = config
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
        setupImageCache()
        loadProducts()
    }

    private func setupCollectionView() {
        collectionView.prefetchDataSource = prefetchDataSource
        collectionView.isPrefetchingEnabled = true

        // Register cell
        collectionView.register(
            OptimizedProductCell.self,
            forCellWithReuseIdentifier: "ProductCell"
        )

        // Performance optimizations
        collectionView.showsVerticalScrollIndicator = false
        collectionView.decelerationRate = UIScrollView.DecelerationRate.fast
    }

    private func setupImageCache() {
        if config.memoryManagement.imageCaching {
            // Configure image cache limits
            imageCache.countLimit = 100
            imageCache.totalCostLimit = 50 * 1024 * 1024 // 50MB
        }
    }

    private func loadProducts() {
        ProductService.fetchProducts { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let products):
                    self?.products = products
                    self?.collectionView.reloadData()
                case .failure(let error):
                    print("Error loading products: \\(error)")
                }
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()

        // Clear image cache on memory warning
        imageCache.removeAllObjects()

        // Reload visible cells to reduce memory usage
        collectionView.reloadItems(
            at: collectionView.indexPathsForVisibleItems
        )
    }
}

// MARK: - UICollectionViewDataSource
extension OptimizedProductViewController: UICollectionViewDataSource {

    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return products.count
    }

    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(
            withReuseIdentifier: "ProductCell",
            for: indexPath
        ) as! OptimizedProductCell

        let product = products[indexPath.item]
        cell.configure(with: product, imageCache: imageCache, config: config)

        return cell
    }
}

// Optimized collection view cell
class OptimizedProductCell: UICollectionViewCell {

    private let imageView = UIImageView()
    private let titleLabel = UILabel()
    private let priceLabel = UILabel()

    private var imageDownloadTask: URLSessionDataTask?

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupViews()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupViews() {
        // Configure image view
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.cornerRadius = 8

        // Configure labels
        titleLabel.font = UIFont.systemFont(ofSize: 16, weight: .medium)
        titleLabel.numberOfLines = 2

        priceLabel.font = UIFont.systemFont(ofSize: 14, weight: .regular)
        priceLabel.textColor = .systemBlue

        // Add to view hierarchy
        [imageView, titleLabel, priceLabel].forEach {
            $0.translatesAutoresizingMaskIntoConstraints = false
            contentView.addSubview($0)
        }

        // Setup constraints
        NSLayoutConstraint.activate([
            imageView.topAnchor.constraint(equalTo: contentView.topAnchor),
            imageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            imageView.trailingAnchor.constraint(equalTo: contentView.trailingAnchor),
            imageView.heightAnchor.constraint(equalTo: imageView.widthAnchor),

            titleLabel.topAnchor.constraint(equalTo: imageView.bottomAnchor, constant: 8),
            titleLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            titleLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor),

            priceLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 4),
            priceLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            priceLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor),
            priceLabel.bottomAnchor.constraint(lessThanOrEqualTo: contentView.bottomAnchor)
        ])
    }

    func configure(with product: Product, imageCache: NSCache<NSString, UIImage>, config: MobilePerformanceConfig) {
        titleLabel.text = product.name
        priceLabel.text = "$\\(product.price)"

        // Cancel previous image download
        imageDownloadTask?.cancel()

        // Load image with caching
        loadImage(
            from: product.imageURL,
            cache: imageCache,
            useCache: config.memoryManagement.imageCaching
        )
    }

    private func loadImage(from url: URL, cache: NSCache<NSString, UIImage>, useCache: Bool) {
        let cacheKey = url.absoluteString as NSString

        // Check cache first
        if useCache, let cachedImage = cache.object(forKey: cacheKey) {
            imageView.image = cachedImage
            return
        }

        // Download image
        imageDownloadTask = URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            guard let data = data, let image = UIImage(data: data) else { return }

            // Cache image
            if useCache {
                cache.setObject(image, forKey: cacheKey)
            }

            DispatchQueue.main.async {
                self?.imageView.image = image
            }
        }

        imageDownloadTask?.resume()
    }

    override func prepareForReuse() {
        super.prepareForReuse()

        // Cancel image download
        imageDownloadTask?.cancel()
        imageDownloadTask = nil

        // Clear image
        imageView.image = nil
    }
}
"""
}