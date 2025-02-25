from .models import TrafficFlow, ServiceEndpoint
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables

class ServiceEndpointTable(NetBoxTable):
    application_name = tables.Column(verbose_name='Application Name')
    service_port = tables.Column(verbose_name='Service Port')
    process_name = tables.Column(verbose_name='Process Name')
    
    class Meta(NetBoxTable.Meta):
        model = ServiceEndpoint
        fields = ('application_name', 'service_port', 'process_name')
        default_columns = ('application_name', 'service_port', 'process_name')
        
class TrafficFlowTable(NetBoxTable):
    timestamp = columns.DateTimeColumn()
    src_ip = tables.Column(verbose_name='Source IP')
    src_object = tables.Column(
        verbose_name='Source Object',
        linkify=True
    )
    dst_ip = tables.Column(verbose_name='Destination IP')
    dst_object = tables.Column(
        verbose_name='Destination Object',
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = TrafficFlow
        fields = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'server_id', 'service_endpoint', 'timestamp')
        default_columns = ('src_ip', 'src_object', 'dst_ip', 'dst_object', 'protocol', 'service_port', 'service_endpoint')