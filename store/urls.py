from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("products", views.ProductViewSet, basename="products")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("customers", views.CustomerViewSet, basename="customer")
router.register("carts", views.CartViewSet, basename="cart")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cartitem")
router.register("orders", views.OrderViewSet, basename="order")

urlpatterns = [] + router.urls + cart_router.urls
