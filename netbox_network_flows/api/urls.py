from rest_framework.routers import DefaultRouter
from .views import TrafficFlowViewSet

router = DefaultRouter()
router.register(r'flows', TrafficFlowViewSet, basename='traffic-flow')

urlpatterns = router.urls