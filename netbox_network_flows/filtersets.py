import django_filters
from .models import ServiceEndpoint, TrafficFlow
from netbox.filtersets import NetBoxModelFilterSet

class ServiceEndpointFilterSet(NetBoxModelFilterSet):
    
    class Meta:
        model = ServiceEndpoint
        fields = ['service_port', 'process_name', 'application_name']

class TrafficFlowFilterSet(NetBoxModelFilterSet):
    
    class Meta:
        model = TrafficFlow
        fields = ['src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'timestamp']