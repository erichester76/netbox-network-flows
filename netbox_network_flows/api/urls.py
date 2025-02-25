from netbox.api.routers import NetBoxRouter
from .views import TrafficFlowViewSet, ServiceEndpointViewSet

router = NetBoxRouter()
router.register('flows', TrafficFlowViewSet)
router.register('service-endpoints', ServiceEndpointViewSet)

urlpatterns = router.urls