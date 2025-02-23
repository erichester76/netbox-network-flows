from rest_framework.routers import DefaultRouter
from .views import TrafficFlowViewSet

router = DefaultRouter()
router.register(r'flows', TrafficFlowViewSet)

urlpatterns = router.urls