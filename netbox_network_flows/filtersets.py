from netbox.filtersets import NetBoxModelFilterSet
from netbox_network_flows.models import ServiceEndpoint, TrafficFlow

class ServiceEndpointFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ServiceEndpoint
        fields = ['service_port', 'process_name', 'application_name']

class TrafficFlowFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = TrafficFlow
        fields = ['src_ip', 'dst_ip', 'protocol', 'service_port', 'server_id', 'timestamp']