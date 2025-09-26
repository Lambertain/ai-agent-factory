"""
E-commerce UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для e-commerce проектов.
Включает специфичные UI компоненты, цветовые схемы и паттерны для онлайн-магазинов.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class EcommerceUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для E-commerce проектов."""

    # Основные настройки
    domain_type: str = "ecommerce"
    project_type: str = "online_store"

    # E-commerce специфичные настройки
    enable_product_cards: bool = True
    enable_shopping_cart: bool = True
    enable_wishlist: bool = True
    enable_product_comparison: bool = True
    enable_reviews_ratings: bool = True

    # Checkout настройки
    enable_guest_checkout: bool = True
    enable_one_click_purchase: bool = True
    enable_abandoned_cart_recovery: bool = True

    # UI специфичные настройки
    product_grid_columns: Dict[str, int] = None
    enable_infinite_scroll: bool = True
    enable_quick_view: bool = True

    def __post_init__(self):
        super().__post_init__()
        if self.product_grid_columns is None:
            self.product_grid_columns = {
                "mobile": 1,
                "tablet": 2,
                "desktop": 4,
                "wide": 5
            }

    def get_color_scheme(self) -> Dict[str, Any]:
        """Цветовая схема для E-commerce."""
        return {
            "primary": "hsl(210, 100%, 50%)",  # Trust blue
            "secondary": "hsl(45, 100%, 55%)", # Action yellow
            "success": "hsl(120, 60%, 45%)",   # Success green
            "warning": "hsl(35, 100%, 50%)",   # Warning orange
            "destructive": "hsl(0, 70%, 50%)", # Error red
            "accent": "hsl(270, 60%, 60%)",    # Accent purple

            # E-commerce specific colors
            "price": "hsl(120, 60%, 35%)",     # Price green
            "discount": "hsl(0, 80%, 55%)",    # Discount red
            "sale": "hsl(45, 95%, 50%)",       # Sale badge
            "stock_low": "hsl(35, 90%, 60%)",  # Low stock warning
            "out_of_stock": "hsl(0, 50%, 60%)", # Out of stock

            # Trust signals
            "verified": "hsl(140, 60%, 45%)",  # Verified seller
            "secure": "hsl(210, 80%, 50%)",    # Secure payment
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для E-commerce."""
        return {
            "product_card": {
                "show_badges": True,
                "show_rating": self.enable_reviews_ratings,
                "show_quick_actions": True,
                "hover_effects": True,
                "image_aspect_ratio": "4:3"
            },
            "navigation": {
                "show_categories": True,
                "show_search": True,
                "show_cart_icon": self.enable_shopping_cart,
                "show_wishlist_icon": self.enable_wishlist,
                "mega_menu": True
            },
            "filters": {
                "sidebar_layout": True,
                "price_range_slider": True,
                "brand_filter": True,
                "rating_filter": self.enable_reviews_ratings,
                "availability_filter": True
            },
            "cart": {
                "mini_cart": True,
                "cart_drawer": True,
                "quantity_selector": True,
                "remove_item": True,
                "save_for_later": True
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для E-commerce."""
        return {
            "grid": {
                "product_grid": self.product_grid_columns,
                "category_grid": {"mobile": 2, "tablet": 3, "desktop": 4},
                "featured_grid": {"mobile": 1, "tablet": 2, "desktop": 3}
            },
            "spacing": {
                "section_gap": "6rem",
                "component_gap": "2rem",
                "element_gap": "1rem"
            },
            "containers": {
                "header": "full",
                "main": "wide",
                "footer": "full"
            }
        }

    def get_animation_config(self) -> Dict[str, Any]:
        """Конфигурация анимаций для E-commerce."""
        return {
            "product_hover": {
                "scale": 1.05,
                "duration": "300ms",
                "easing": "ease-out"
            },
            "add_to_cart": {
                "type": "bounce",
                "duration": "600ms"
            },
            "page_transitions": {
                "type": "fade",
                "duration": "200ms"
            },
            "loading_states": {
                "skeleton": True,
                "shimmer": True,
                "progress_bars": True
            }
        }

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Конфигурация accessibility для E-commerce."""
        return {
            "high_contrast_mode": True,
            "keyboard_navigation": True,
            "screen_reader_optimized": True,
            "focus_indicators": True,
            "aria_labels": {
                "product_card": "Product: {name}, Price: {price}",
                "add_to_cart": "Add {product} to cart",
                "remove_from_cart": "Remove {product} from cart",
                "rating": "{rating} out of 5 stars"
            },
            "skip_links": [
                {"href": "#main", "label": "Skip to main content"},
                {"href": "#products", "label": "Skip to products"},
                {"href": "#filters", "label": "Skip to filters"}
            ]
        }


# Пример использования
def get_ecommerce_uiux_dependencies() -> EcommerceUIUXDependencies:
    """Создать конфигурацию для E-commerce проекта."""
    return EcommerceUIUXDependencies(
        api_key="your-api-key",
        domain_type="ecommerce",
        project_type="online_store",
        enable_product_cards=True,
        enable_shopping_cart=True,
        enable_wishlist=True,
        enable_reviews_ratings=True,
        enable_quick_view=True
    )


# Пример использования в React компоненте
ECOMMERCE_COMPONENT_EXAMPLES = {
    "product_card": """
// E-commerce Product Card Component
export function EcommerceProductCard({ product, config }: {
  product: Product;
  config: EcommerceUIUXDependencies;
}) {
  const colorScheme = config.get_color_scheme();
  const componentConfig = config.get_component_config().product_card;

  return (
    <Card className="group overflow-hidden">
      <div className="relative aspect-[4/3] overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
        />

        {componentConfig.show_badges && product.badges && (
          <div className="absolute top-2 left-2 flex flex-col gap-1">
            {product.badges.map(badge => (
              <Badge
                key={badge}
                style={{ backgroundColor: colorScheme.sale }}
                className="text-xs font-bold"
              >
                {badge}
              </Badge>
            ))}
          </div>
        )}

        {componentConfig.show_quick_actions && (
          <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
            <Button size="sm" variant="secondary">
              <Eye className="w-4 h-4" />
              Quick View
            </Button>
            <Button size="sm" variant="secondary">
              <Heart className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>

      <CardContent className="p-4">
        <h3 className="font-semibold line-clamp-2 mb-2">{product.name}</h3>

        {componentConfig.show_rating && product.rating && (
          <div className="flex items-center gap-1 mb-2">
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={cn(
                    "w-4 h-4",
                    i < product.rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"
                  )}
                />
              ))}
            </div>
            <span className="text-sm text-muted-foreground">({product.reviewCount})</span>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span
              className="text-lg font-bold"
              style={{ color: colorScheme.price }}
            >
              ${product.price}
            </span>
            {product.originalPrice && (
              <span className="text-sm text-muted-foreground line-through">
                ${product.originalPrice}
              </span>
            )}
          </div>

          <Button
            size="sm"
            style={{ backgroundColor: colorScheme.primary }}
            className="text-white"
          >
            <ShoppingCart className="w-4 h-4 mr-1" />
            Add to Cart
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
""",

    "shopping_cart": """
// E-commerce Shopping Cart Component
export function EcommerceShoppingCart({ config }: {
  config: EcommerceUIUXDependencies;
}) {
  const colorScheme = config.get_color_scheme();
  const cartConfig = config.get_component_config().cart;

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline" size="icon" className="relative">
          <ShoppingCart className="h-4 w-4" />
          <Badge
            className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs"
            style={{ backgroundColor: colorScheme.accent }}
          >
            3
          </Badge>
        </Button>
      </SheetTrigger>

      <SheetContent className="w-[400px] sm:w-[540px]">
        <SheetHeader>
          <SheetTitle>Shopping Cart</SheetTitle>
        </SheetHeader>

        <div className="flex flex-col h-full">
          <div className="flex-1 overflow-auto py-4">
            {/* Cart Items */}
            <div className="space-y-4">
              {cartItems.map(item => (
                <div key={item.id} className="flex gap-3 p-3 border rounded-lg">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-16 h-16 object-cover rounded"
                  />

                  <div className="flex-1">
                    <h4 className="font-medium line-clamp-1">{item.name}</h4>
                    <p className="text-sm text-muted-foreground">Size: {item.size}</p>

                    <div className="flex items-center justify-between mt-2">
                      {cartConfig.quantity_selector && (
                        <div className="flex items-center gap-2">
                          <Button size="sm" variant="outline">-</Button>
                          <span className="w-8 text-center">{item.quantity}</span>
                          <Button size="sm" variant="outline">+</Button>
                        </div>
                      )}

                      <span
                        className="font-semibold"
                        style={{ color: colorScheme.price }}
                      >
                        ${item.price * item.quantity}
                      </span>
                    </div>
                  </div>

                  {cartConfig.remove_item && (
                    <Button size="sm" variant="ghost">
                      <X className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Cart Summary */}
          <div className="border-t pt-4 space-y-4">
            <div className="flex justify-between">
              <span>Subtotal:</span>
              <span className="font-semibold">${subtotal}</span>
            </div>
            <div className="flex justify-between">
              <span>Shipping:</span>
              <span>${shipping}</span>
            </div>
            <div className="flex justify-between text-lg font-bold">
              <span>Total:</span>
              <span style={{ color: colorScheme.price }}>${total}</span>
            </div>

            <Button
              className="w-full"
              style={{ backgroundColor: colorScheme.primary }}
            >
              Proceed to Checkout
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
"""
}