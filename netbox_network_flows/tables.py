from .models import TrafficFlow, ServiceEndpoint
from netbox.tables import NetBoxTable, columns
import django_tables2 as tables


class ServiceEndpointTable(tables.Table):
    application_name = tables.Column()
    service_port = tables.Column()
    process_name = tables.Column()
    flow_count = tables.LinkColumn('trafficflow_by_endpoint_list', args=[tables.A('id')], verbose_name='Flows')

    class Meta:
        model = ServiceEndpoint
        fields = ('application_name', 'service_port', 'process_name', 'flow_count')
        orderable = True
        
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