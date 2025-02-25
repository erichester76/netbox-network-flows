from netbox.api.routers import NetBoxRouter
from .views import TrafficFlowViewSet, ServiceEndpointViewSet

app_name = 'netbox_network_flows'

router = NetBoxRouter()
router.register('flows', TrafficFlowViewSet)
router.register('service-endpoints', ServiceEndpointViewSet)

urlpatterns = router.urls