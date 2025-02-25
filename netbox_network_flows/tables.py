from .models import TrafficFlow, ServiceEndpoint
from netbox.tables import NetBoxTable


class ServiceEndpointTable(NetBoxTable):

    class Meta(NetBoxTable.Meta):
        model = ServiceEndpoint
        fields = ('pk', 'id', 'application_name', 'service_port', 'process_name', 'created', 'last_updated')
        default_columns = ('application_name', 'service_port', 'process_name')
        orderable = True
        
class TrafficFlowTable(NetBoxTable):
    
    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('pk', 'id','src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'service_endpoint', 'timestamp', 'created', 'last_updated')
        default_columns = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'service_endpoint')