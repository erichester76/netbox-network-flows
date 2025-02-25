import django_filters
from .models import ServiceEndpoint, TrafficFlow
from netbox.filtersets import NetBoxModelFilterSet

class ServiceEndpointFilterSet(NetBoxModelFilterSet):
    service_port = django_filters.NumberFilter(field_name='service_port', lookup_expr='exact')
    process_name = django_filters.CharFilter(field_name='process_name', lookup_expr='iexact')
    application_name = django_filters.CharFilter(field_name='application_name', lookup_expr='icontains')

    class Meta:
        model = ServiceEndpoint
        fields = ['service_port', 'process_name', 'application_name']

class TrafficFlowFilterSet(NetBoxModelFilterSet):
    src_ip = django_filters.CharFilter(field_name='src_ip', lookup_expr='exact')
    dst_ip = django_filters.CharFilter(field_name='dst_ip', lookup_expr='exact')
    protocol = django_filters.CharFilter(field_name='protocol', lookup_expr='exact')
    service_port = django_filters.NumberFilter(field_name='service_port', lookup_expr='exact')
    server_id = django_filters.CharFilter(field_name='server_id', lookup_expr='exact')
    timestamp = django_filters.NumberFilter(field_name='timestamp', lookup_expr='exact')

    class Meta:
        model = TrafficFlow
        fields = ['src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'timestamp']