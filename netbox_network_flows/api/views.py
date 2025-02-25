from ..models import TrafficFlow, ServiceEndpoint
from .serializers import TrafficFlowSerializer, ServiceEndpointSerializer
from ..filtersets import ServiceEndpointFilterSet, TrafficFlowFilterSet
from django.db.models import Count 
from netbox.api.viewsets import NetBoxModelViewSet

class TrafficFlowViewSet(NetBoxModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    filterset_class = TrafficFlowFilterSet

class ServiceEndpointViewSet(NetBoxModelViewSet):
    queryset = ServiceEndpoint.objects.all()
    serializer_class = ServiceEndpointSerializer
    filterset_class = ServiceEndpointFilterSet
