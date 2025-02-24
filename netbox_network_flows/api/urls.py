from rest_framework.routers import DefaultRouter
from .views import TrafficFlowViewSet, ServiceEndpointsViewSet

router = DefaultRouter()
router.register(r'flows', TrafficFlowViewSet)
router.register('service-endpoints', ServiceEndpointsViewSet)

urlpatterns = router.urls