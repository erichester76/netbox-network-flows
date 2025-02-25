from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from netbox_network_flows.models import TrafficFlow, ServiceEndpoint
from .serializers import TrafficFlowSerializer, ServiceEndpointSerializer
from ..filtersets import ServiceEndpointFilterSet, TrafficFlowFilterSet
from django.db.models import Count 

class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    filterset_class = TrafficFlowFilterSet

class ServiceEndpointViewSet(viewsets.ModelViewSet):
    queryset = ServiceEndpoint.objects.all()
    serializer_class = ServiceEndpointSerializer
    filterset_class = ServiceEndpointFilterSet
