from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')


urlpatterns = [] + router.urls










