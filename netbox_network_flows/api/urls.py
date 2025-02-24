from rest_framework.routers import DefaultRouter
from .views import TrafficFlowViewSet, ServiceEndpointViewSet

router = DefaultRouter()
router.register(r'flows', TrafficFlowViewSet)
router.register('service-endpoints', ServiceEndpointViewSet)

urlpatterns = router.urls