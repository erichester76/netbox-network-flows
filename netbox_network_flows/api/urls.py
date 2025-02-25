from netbox.api.routers import NetBoxRouter
from .views import TrafficFlowViewSet, ServiceEndpointViewSet

router = NetBoxRouter()
router.register(r'flows', TrafficFlowViewSet)
router.register(r'service-endpoints', ServiceEndpointViewSet)

urlpatterns = router.urls