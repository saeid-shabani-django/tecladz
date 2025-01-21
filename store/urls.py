from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')
router.register('categories',views.CategoryViewSet,basename='category')

urlpatterns = [] + router.urls










